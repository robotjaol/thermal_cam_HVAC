# Thermal Camera HVAC

> PLC SCSL Laboratory Project Base Learning

### General Diagram Plan

Here's the diagram that i made

![img](doc/img/diagram_plan.png)

In this diagram, there are three important components for building this project. Firstly, a thermal camera is used to measure people's temperature in the laboratory. Secondly, a mini PC is utilized to control and calculate the temperature obtained from the camera. Lastly, a universal remote control is employed to adjust or regulate the airflow emitted by the AC.

### General Flowchart

![img](doc/img/flowchart.png)

So, this is a simple explanation about the flowchart. In this flowchart diagram, it starts with the thermal camera measuring people's temperature, and then the temperature data is controlled and calculated by the mini PC. When the people's temperature exceeds the reference temperature, the universal remote will increase the airflow from the AC. Conversely, when the people's temperature falls below the reference temperature, the universal remote control will decrease the airflow from the AC.

### General Electrical Architecture

![img](doc/img/electrical_architecture.png)

This is a simple explanation of the general electrical architecture. i will explain how to wire those three important components

### General Communication Architecture
In this section, the communication architecture explains how those three components can comunicate with each other

---

### Thermal Camera to Raspberry Pi diagram


Here is how to wire Thermal Camera to raspberry Pi
### Universal Remote Control Diagram
#### For Receiving
![Diagram](doc/img/ur_receiver.png)

In this diagram, I am using an Arduino Nano to retrieve multiple data from various devices like AC, TV, and others

#### for Transmission
![Diagram](doc/img/ur_transmitter.png)

In this diagram, I use Arduino to transmit and adjust values back to many devices

#### For Triggered Transfer
![Diagram](doc/img/ur_trigger.png)

The trigger diagram is used to generate triggers for the Arduino transmitter to adjust values transmitted to other devices, using RX TX.

### Component You need it for this Project

#### 1. Mini PC
- Rasberry 4 RAM 8GB [here](https://shp.ee/sb0f2v0)

#### 2. Thermal Camera
- InfiRAY T3S [here](https://tokopedia.link/vz7A5uvbfIb)

#### 3. Universal Remote
- Arduino NANO (3, For Transmission and trigger from Raspberry Pi )

- IR Receiver (A lot)

- IR LED Tactile Button

- 1K Resistor

- 100E Resistor

- Bread Board or PCB

- Cable or Jumper

## Reference that i collected from internet

- Thermal camera sensor [here](https://learn.adafruit.com/adafruit-amg8833-8x8-thermal-camera-sensor)

- basic website how2electronics [here](https://how2electronics.com/diy-thermal-camera-with-raspberry-pi-amg8833-sensor/)

- Github reference AMG8833 [here](https://github.com/adafruit/Adafruit_AMG88xx_python)

- Raspberry pi and amg8833 [here](https://how2electronics.com/diy-thermal-camera-with-raspberry-pi-amg8833-sensor/)

- Adafruit AMG8833 [here](https://github.com/adafruit/Adafruit_AMG88xx_python)

- How To Electronics [here](https://www.youtube.com/watch?v=piVV-5RuX2o)

- Usinng AMG8833 [here](https://github.com/makerportal/AMG8833_IR_cam)

- Maker Portal [here](https://github.com/makerportal)

- RGM Vision avaiable [here](https://www.rgmvision.com/infrared-computer-vision/)

- Acsess webinar here [here](https://www.youtube.com/watch?v=0o2d46kyR1Q)

- For source code [here](https://pyimagesearch.com/2022/10/10/introduction-to-infrared-vision-near-vs-mid-far-infrared-images/)

- PyImage Search [here](https://pyimagesearch.com/2022/10/24/thermal-vision-fever-detector-with-python-and-opencv-starter-project/)

- AI Thermometer [here](https://github.com/tomasz-lewicki/ai-thermometer)

- How to build universal remoe [here](https://www.youtube.com/watch?v=m7z4CU5mw9E)