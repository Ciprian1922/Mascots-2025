The used components for this project are listed bellow:

| Component                             | Purpose                                                                |
| ------------------------------------- | ---------------------------------------------------------------------- |
| **Raspberry Pi 4B**                   | Central controller running the main code and hosting the server        |
| **SG90 Servo Motor**                  | Rotates the dispensing gate to release food                            |
| **DVD disc (modified)**               | Used as a rotating gate for cereal dispensing                          |v
| **PCA9685 Servo Driver (16-channel)** | Provides stable PWM signals to servo                                   |
| **HX711 Load Cell Amplifier**         | Amplifies signal from load cell                                        |
| **Load Cell (2kg)**                   | Measures weight of the bowl to determine food presence and consumption |
| **HP USB Webcam**                     | Captures images/videos during feeding sessions                         |
| **Power Bank (DIY, 5V output)**       | Powers components independently from Raspberry Pi’s GPIO pins          |
| **Vibrating Motor**                   | Attached to prevent or resolve jamming of food in the dispenser        |
| **Dupont Jumper Wires (Male-Male)**   | Connections between all electronic components                          |
| **Breadboard**                        | Prototyping and distribution of power/signal lines                     |
| **MicroSD Card (16GB or higher)**     | Contains Raspberry Pi OS and software                                  |
| **Ethernet Cable / Wi-Fi Dongle**     | For remote access (via Tailscale VPN)                                  |


| Component                                              | Purpose                                                                 |
| ------------------------------------------------------ | ----------------------------------------------------------------------- |
| **Capacitive Soil Moisture Sensor**                    | Detects moisture level in the soil                                      |
| **MCP3008 ADC**                                        | Converts analog signal from moisture sensor to digital for Raspberry Pi |
| **Water Pump (5V or 12V, submersible or peristaltic)** | Pumps water to the plant based on moisture levels                       |
| **Relay Module or Transistor (MOSFET)**                | Controls water pump switching from Raspberry Pi                         |
| **Water Tubing / Hose**                                | Directs water from reservoir to plant pot                               |
| **Water Reservoir (Bottle or Container)**              | Stores water for irrigation                                             |
| **Diode (e.g., 1N4007)**                               | Flyback protection for pump motor                                       |
| **Resistors / Capacitors**                             | (Optional) For voltage stabilization/filtering in analog circuit        |

For future work, these will be added on over the existing components:


| Component                                          | Purpose                                                                   |
| -------------------------------------------------- | ------------------------------------------------------------------------- |
| **NFC Reader (e.g., PN532)**                       | For identifying individual pets (planned)                                 |
| **Gyroscope/Accelerometer Sensor (e.g., MPU6050)** | Tracks cat’s movement, sleeping, grooming patterns (for future ML models) |
| **YOLOv5 Object Detection Model (deployed on Pi)** | For multi-cat recognition via camera                                      |
| **Neck-Worn Smart Tag (custom)**                   | Wearable for activity tracking                                            |
| **Solar Panel (5W, optional)**                     | For future energy self-sufficiency                                        |
| **Real-Time Clock (RTC Module)**                   | For time-based logging if no internet is available                        |
