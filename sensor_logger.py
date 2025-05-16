import os
import time
import sqlite3
import threading
import board
import busio
import digitalio
import RPi.GPIO as GPIO
from hx711 import HX711
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
from adafruit_mcp3xxx.mcp3008 import MCP3008
from adafruit_mcp3xxx.analog_in import AnalogIn

# Configuration
DATABASE = 'pet_plant.db'
RELAY_PIN = 21
DT_PIN = 5
SCK_PIN = 6
CS_PIN = 26

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def init_db():
    """Initialize or reset database"""
    if os.path.exists(DATABASE):
        try:
            conn = sqlite3.connect(DATABASE)
            conn.execute("SELECT * FROM sensor_data LIMIT 1")
            conn.execute("SELECT * FROM feed_history LIMIT 1")
            conn.execute("SELECT * FROM water_history LIMIT 1")
            conn.close()
        except sqlite3.OperationalError:
            os.remove(DATABASE)

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.executescript('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            weight REAL,
            moisture INTEGER,
            voltage REAL
        );
        CREATE TABLE IF NOT EXISTS feed_history (
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS water_history (
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    conn.close()

class WeightSensor:
    def _init_(self):
        self.hx = HX711(DT_PIN, SCK_PIN)
        self.hx.set_reading_format("MSB", "MSB")
        
        print("⚖️ Calibrating weight sensor...")
        start = time.time()
        while not self.hx.is_ready():
            if time.time() - start > 10:
                raise RuntimeError("Weight sensor not found")
            time.sleep(0.1)
        
        self.hx.reset()
        self.hx.tare()
        self.hx.set_reference_unit(-441)  # Adjust this value

    def get_weight(self):
        try:
            return max(0, int(self.hx.get_weight(5)))
        except Exception as e:
            print(f"Weight error: {str(e)}")
            return None

class MoistureSensor:
    def _init_(self):
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        cs = digitalio.DigitalInOut(board.D26)
        self.mcp = MCP3008(spi, cs)
        self.chan = AnalogIn(self.mcp, 0)
        
    def read(self):
        try:
            return self.chan.value, self.chan.voltage
        except Exception as e:
            print(f"Moisture error: {str(e)}")
            return None, None

class Actuators:
    def _init_(self):
        # Servo setup
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.pca = PCA9685(self.i2c)
        self.pca.frequency = 50
        self.servo = servo.Servo(self.pca.channels[0], 
                               min_pulse=500, max_pulse=2500)
        
        # Relay setup
        GPIO.setup(RELAY_PIN, GPIO.OUT)
        GPIO.output(RELAY_PIN, GPIO.LOW)

    def feed_cat(self):
        try:
            self.servo.angle = 90
            time.sleep(1)
            self.servo.angle = 0
            return True
        except Exception as e:
            print(f"Feeding error: {str(e)}")
            return False

    def water_plant(self):
        try:
            GPIO.output(RELAY_PIN, GPIO.HIGH)
            time.sleep(2)
            GPIO.output(RELAY_PIN, GPIO.LOW)
            return True
        except Exception as e:
            print(f"Watering error: {str(e)}")
            return False

def sensor_loop(weight_sensor, moisture_sensor):
    """Continuous sensor monitoring"""
    conn = sqlite3.connect(DATABASE)
    while True:
        weight = weight_sensor.get_weight()
        moisture, voltage = moisture_sensor.read()
        
        if None not in (weight, moisture, voltage):
            conn.execute('''
                INSERT INTO sensor_data (weight, moisture, voltage)
                VALUES (?, ?, ?)
            ''', (weight, moisture, voltage))
            conn.commit()
            print(f"📊 Weight: {weight}g | Moisture: {moisture} | Voltage: {voltage:.2f}V")
        
        time.sleep(1)

def action_handler(actuators):
    """Process queued actions"""
    conn = sqlite3.connect(DATABASE)
    while True:
        try:
            row = conn.execute('''
                SELECT rowid, type FROM actions 
                ORDER BY timestamp LIMIT 1
            ''').fetchone()
            
            if row:
                action_id, action_type = row
                success = False
                
                if action_type == 'feed':
                    success = actuators.feed_cat()
                elif action_type == 'water':
                    success = actuators.water_plant()
                
                if success:
                    conn.execute("DELETE FROM actions WHERE rowid = ?", (action_id,))
                    conn.commit()
                    print(f"✅ {action_type.capitalize()} action completed")
                
        except sqlite3.OperationalError:
            # Create actions table if missing
            conn.execute('''
                CREATE TABLE IF NOT EXISTS actions (
                    type TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
        
        time.sleep(1)

if _name_ == '_main_':
    init_db()
    actuators = Actuators()
    weight_sensor = WeightSensor()
    moisture_sensor = MoistureSensor()

    # Start threads
    threading.Thread(target=sensor_loop, args=(weight_sensor, moisture_sensor), daemon=True).start()
    threading.Thread(target=action_handler, args=(actuators,), daemon=True).start()

    # Keep main thread alive
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("🚨 System stopped")
