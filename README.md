# Thermal CCTV HVAC
PLC SCSL Laboratory Project Base Learning

### General Diagram Plan

Here's the diagram that i made

![img](doc/img/diagram_plan.png)

- In this diagram, there are three important components for building this project. Firstly, a thermal camera is used to measure people's temperature in the laboratory. Secondly, a mini PC is utilized to control and calculate the temperature obtained from the camera. Lastly, a universal remote control is employed to adjust or regulate the airflow emitted by the AC.

#### Device looks like

![img](doc/img/device.png)

system looks like this

### General Flowchart

![img](doc/img/flowchart.png)

- So, this is a simple explanation about the flowchart. In this flowchart diagram, it starts with the thermal camera measuring people's temperature, and then the temperature data is controlled and calculated by the mini PC. When the people's temperature exceeds the reference temperature, the universal remote will increase the airflow from the AC. Conversely, when the people's temperature falls below the reference temperature, the universal remote control will decrease the airflow from the AC.

### General Electrical Architecture

![img](doc/img/electrical_architecture.png)

- This is a simple explanation of the general electrical architecture. i will explain how to wire those three important components

### General Communication Architecture

- In this section, the communication architecture explains how those three components can comunicate with each other

![img](doc/img/communication_architecture.png)
---



Here is how to wire Thermal Camera to Mini PC

## Mini PC Comparison Description 
### Jetson Nano vs Intel NUC i7

This README provides a comparison between Jetson Nano and Intel NUC i7, highlighting their features, advantages, disadvantages, and conclusions.

### Jetson Nano

#### Advantages:
- Specifically designed for AI and edge computing.
- Equipped with a powerful NVIDIA GPU for accelerated AI computations.
- Compact size and energy-efficient.
- Ideal for computer vision applications, including object detection and thermal analysis.

#### Shortcomings:
- Limited computing power compared to Intel NUC i7.
- Lack of official Windows support (though unofficial installation is possible).

### Intel NUC i7

#### Advantages:
- High performance with Intel Core i7 processor.
- Official Windows support.
- Multiple I/O ports for external device connections.
- Suitable for data processing, server, and thermal analysis applications.

#### Shortcomings:
- Larger size compared to Jetson Nano.
- Higher power consumption.

### Conclusion:
- For those prioritizing high performance and official Windows compatibility, the Intel NUC i7 emerges as the preferred choice.
- Alternatively, individuals focused on AI edge computing and compact design may find the Jetson Nano more suitable for their needs.


### Universal Remote Control Diagram
#### For Receiving
![Diagram](doc/img/ur_receiver.png)

In this diagram, I am using an Arduino Nano to retrieve multiple data from various devices like AC, TV, and others

#### for Transmission
![Diagram](doc/img/ur_transmitter.png)

In this diagram, I use Arduino to transmit and adjust values back to many devices

#### For Wiring Mini PC to Universal Remote
![Diagram](doc/img/ur_trigger.png)

The communication diagram is used to generate triggers for the Arduino transmitter to adjust values transmitted to other devices, using W5500.

### Component You need it for this Project

follow this [link for components](https://docs.google.com/spreadsheets/d/1vpriAi5HHOCgwNC7Mt6s1HICf34Qzx8J2fEp0PEnn2U/edit#gid=0)

### Task 

- [ ] Cari CCTV dengan capture yang lebih besar dari sebelumnya (PROGRESS)
   
- [x] Ubah Diagram ELC dan Communication

- [ ] Comparison JETSON dan NUC [Link Comparison Here](https://docs.google.com/spreadsheets/d/1smyAvMr5_zLs4XbiOqaG5MXrTgi8uHW2DJUwPbSx77A/edit?hl=id#gid=0)

- [ ] Fix UI control Web Stream Lit

- [x] Datasheet Component

- [x] Value IR dan tipe data [HEX]

- [ ] Komunikasi data hardware (PROGRESS)

Question (PROGRESS)

- [ ] Kondisi AC on/off jika sudah ada aliran listrik 

## Reference that i collected from internet

- Thermal camera AMG8833 sensor [here](https://learn.adafruit.com/adafruit-amg8833-8x8-thermal-camera-sensor)

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

- website to build universal remote [here](https://www.viralsciencecreativity.com/post/universal-ir-remote-controller)

- Thermal Camera TC100 [here](https://github.com/leswright1977/PyThermalCamera/)
