# Thermal CCTV HVAC

PLC SCSL Laboratory Project Base Learning [report](https://itsacid-my.sharepoint.com/:w:/g/personal/2040221004_student_its_ac_id/EbupkjB1esBMlMnZHS9zQ2QBUzxRnBv61q4FnL3q58EvzA?e=yw7i2B)

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

## ![img](doc/img/communication_architecture.png)

Here is how to wire Thermal Camera to Mini PC

## Mini PC Comparison Description

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

> if you currently use ESP32 PIN out

![ESP32](doc/img/ESP32.png)

#### for Transmission

![Diagram](doc/img/ur_transmitter.png)

In this diagram, I use Arduino to transmit and adjust values back to many devices

#### For Wiring Mini PC to Universal Remote

![Diagram](doc/img/ur_trigger.png)

The communication diagram is used to generate triggers for the Arduino transmitter to adjust values transmitted to other devices, using W5500.

#### Alternatif Wiring 
![img](doc/img/ESP32-W5500.jpg)

Pin communication wiring 

| ESP32                              | W5500 |
|------------------------------------|-------|
| D5                                 | CS    |
| D18                                | SCK   |
| D19                                | MISO  |
| D23                                | MOSI  |
| 3.3v (better with external 200mha) | VCC   |
| GND                                | GND   |

## Setting IP
- sudo ip addr add 192.168.1.100/24 dev eno1

- sudo ip link set eno1 up

Or you guys can use 

- sudo nano /etc/netplan/01-netcfg.yaml

and input this code 

-    network:
  version: 2
  ethernets:
    eno1:
      dhcp4: no
      addresses:
        - 192.168.1.100/24
      gateway4: 192.168.1.1
      nameservers:
        addresses:
          - 8.8.8.8
          - 8.8.4.4

then type this command in terminal Ctrl+O, Enter, then Ctrl+X

type this command to 

- sudo netplan apply
 
and tes using

- ifconfig


### Component You need it for this Project

follow this [link for components](https://docs.google.com/spreadsheets/d/1vpriAi5HHOCgwNC7Mt6s1HICf34Qzx8J2fEp0PEnn2U/edit#gid=0)

### Task

- [x] industrial CCTV thermal
      
- [x] Modify Electrical and Communication Diagram

- [ ] State Control System Projcet

- [ ] State control System Data transmission

- [ ] Compare JETSON and NUC [Link Comparison Here](https://docs.google.com/spreadsheets/d/1smyAvMr5_zLs4XbiOqaG5MXrTgi8uHW2DJUwPbSx77A/edit?hl=id#gid=0)

- [ ] Fix UI control React x Flask x YOLO

- [x] Client Server via TCP

- [x] Value of IR AC [HEX]

- [X] Hardware data communication 

Question (PROGRESS)

- [ ] AC condition on/off if there is electricity flow

## Reference that i collected from internet

### CCTV Thermal Reference

- Thermal camera AMG8833 sensor [here](https://learn.adafruit.com/adafruit-amg8833-8x8-thermal-camera-sensor)

- Maker Portal [here](https://github.com/makerportal)

- RGM Vision avaiable [here](https://www.rgmvision.com/infrared-computer-vision/)

- Acsess webinar here [here](https://www.youtube.com/watch?v=0o2d46kyR1Q)

- For source code [here](https://pyimagesearch.com/2022/10/10/introduction-to-infrared-vision-near-vs-mid-far-infrared-images/)

- PyImage Search [here](https://pyimagesearch.com/2022/10/24/thermal-vision-fever-detector-with-python-and-opencv-starter-project/)

- AI Thermometer [here](https://github.com/tomasz-lewicki/ai-thermometer)

- Thermal Camera TC100 [here](https://github.com/leswright1977/PyThermalCamera/)

### Universal Remote Reference

- How to build universal remote [here](https://www.youtube.com/watch?v=m7z4CU5mw9E)

- Universal remote reference [here](https://ieeexplore.ieee.org/document/8075906)

- IR Remote explanation [link](https://github.com/Arduino-IRremote/Arduino-IRremote)

- controlling AC using ESP32 [here](https://www.makerguides.com/control-air-conditioner-via-ir-with-esp32-esp8266/)

- arduino reference [here](https://www.electronicshub.org/diy-universal-remote-using-arduino/)

- Compeleted hacksterio [here](https://www.hackster.io/sainisagar7294/arduino-based-universal-tv-remote-09af2d)

- Septa reference [here](https://youtu.be/_nm4if-lusI?si=m2NDjdd2vk4Lo-Tv)


### Website Project

- website to build universal remote [here](https://www.viralsciencecreativity.com/post/universal-ir-remote-controller)

- Website Python Flask [here](https://pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/)

- Website Python [Streamlit](https://github.com/petermartens98/Streamlit-OpenCV-Webcam-Display-Web-App)

### Microcontroller to PC communication

- Youtube Tutorial using [W5500](https://www.youtube.com/watch?v=kB0jZ2dh_vA)

- Website tutorial using [W5500](https://mischianti.org/esp32-ethernet-w5500-with-plain-http-and-ssl-https/) 

- W5500 [library](https://www.arduino.cc/reference/en/libraries/ethernet2/)

### Exentension Project 
- Buzzer active [here](https://diyi0t.com/active-passive-buzzer-arduino-esp8266-esp32/)
