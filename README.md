# ESP32-UWB-Indoor-Location-Tracker

Real-time indoor positioning system using Ultra-Wideband (UWB), ESP32-S3, and Python. The system uses Two-Way Ranging (TWR) and trilateration algorithms to estimate and visualize the position of a mobile tracking tag in real time.

---

## Overview

Traditional GPS systems experience significant accuracy degradation indoors due to signal attenuation and multipath effects. This project demonstrates an indoor localization system using Ultra-Wideband (UWB) technology and a three-anchor architecture to achieve high-accuracy positioning.

<p align="center">
  <img width="450" alt="Image (2)" src="https://github.com/user-attachments/assets/7446f019-2fb9-4378-aecf-82c7fecc768e" />
</p>

The Python application calculates the tag's XY coordinates using trilateration and displays position updates in real time. Historical position data is shown to visualize movement throughout the tracking area.

### Project Highlights

- 3 Fixed UWB Anchors
- 1 Mobile UWB Tag
- ESP32-S3 + DW3000 UWB Hardware
- Python-Based Visualization Software
- Custom CAD Enclosure Design
- Real-Time Position Tracking

---

## Hardware Prototype

<p align="center">
<img width="450"  alt="image" src="https://github.com/user-attachments/assets/8824815a-f645-478c-9003-a3f6673fedb9" />
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/cfc13495-5625-4653-baae-b7375379653a" width="550">
</p>

The system consists of four MakerFab UWB development boards configured as one mobile tracking tag and three fixed anchors. Distance measurements are collected using UWB ranging and transmitted to a host computer for position calculation and visualization.

---

## Hardware

### Main Components

- ESP32-S3 Microcontroller
- Qorvo DW3000 UWB Transceiver
- OLED Display
- LiPo Battery
- USB-C Connectivity

---

## CAD Design

### Front View

<p align="center">
  <img src="https://github.com/user-attachments/assets/7fbdb8f2-27fb-4e7e-9e67-0b6fbd053055" width="450">
</p>

<p align="center">
<img width="450" height="450" alt="image" src="https://github.com/user-attachments/assets/bc65d8cc-df3c-49e1-a864-3b73bb3b4c4d" />
</p>

<p align="center">
<img width="450" height="450" alt="image" src="https://github.com/user-attachments/assets/0ffc220c-64c6-4e36-b965-6adf4946c4b8" />
</p>

### Rear View

<p align="center">
  <img src="https://github.com/user-attachments/assets/a8db6bdf-002b-4d37-a67b-e771ec66a8eb" width="450">
</p>

<p align="center">
<img width="396" height="429" alt="image" src="https://github.com/user-attachments/assets/88153422-e370-4b6e-bc25-d37f85ddb9a0" />
</p>

A custom enclosure was designed to protect the mobile tracking hardware while maintaining portability and accessibility to charging and display interfaces.

---

## System Architecture

```text
          Anchor A0
               ▲
               │
               │
Anchor A2 ◄── Tag ──► Anchor A1
               │
               ▼

          Laptop / Python GUI
```

### Operation

1. The tag communicates with all anchors using UWB Two-Way Ranging (TWR)
2. Distances between anchors and tag are measured
3. Measured ranges are transmitted to a host PC
4. Trilateration algorithms calculate the tag position
5. The calculated coordinates are displayed in real time on the GUI

---

## Software

### Embedded Firmware

- Arduino IDE
- C/C++
- ESP32-S3 Configuration
- UWB Communication Handling

### Python Application

- Serial Data Acquisition
- Range Parsing
- Trilateration Calculations
- Coordinate Smoothing
- Real-Time Visualization

---

## Skills Demonstrated

- Embedded Systems
- Wireless Communications
- Ultra-Wideband (UWB)
- ESP32 Development
- Python Programming
- Serial Communications
- Trilateration Algorithms
- Real-Time Data Visualization
- Hardware Validation & Testing
- CAD Design (SolidWorks)

---

## Future Improvements

- Additional anchor support
- Improved update rate and reduced latency
- 3D position tracking
- Enhanced filtering algorithms
- Custom PCB-based UWB nodes

---

## Author

Anthony Garcia

Electrical Engineering • Embedded Systems • Wireless Communications • RF Engineering
