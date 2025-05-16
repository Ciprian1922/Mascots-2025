from flask import Flask, render_template
import sqlite3
from datetime import datetime



app = Flask(_name_)
DATABASE = 'pet_plant.db'

def get_status():
    conn = sqlite3.connect(DATABASE)
    data = conn.execute('''
        SELECT weight, moisture, voltage 
        FROM sensor_data 
        ORDER BY timestamp DESC LIMIT 1
    ''').fetchone() or (0, 0, 0)
    
    last_feed = conn.execute('''
        SELECT timestamp FROM feed_history 
        ORDER BY timestamp DESC LIMIT 1
    ''').fetchone()
    
    last_water = conn.execute('''
        SELECT timestamp FROM water_history 
        ORDER BY timestamp DESC LIMIT 1
    ''').fetchone()
    
    conn.close()
    return {
        'weight': data[0],
        'moisture': data[1],
        'voltage': round(data[2], 2),
        'last_feed': last_feed[0] if last_feed else 'Never',
        'last_water': last_water[0] if last_water else 'Never'
    }

@app.route('/')
def index():
    return render_template('index.html', **get_status())

@app.route('/action/<type>', methods=['POST'])
def log_action(type):
    conn = sqlite3.connect(DATABASE)
    conn.execute(f"INSERT INTO {type}_history DEFAULT VALUES")
    conn.execute("INSERT INTO actions (type) VALUES (?)", (type,))
    conn.commit()
    conn.close()
    return '', 204

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=5000)
