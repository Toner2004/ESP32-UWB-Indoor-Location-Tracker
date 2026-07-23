# ESP32-UWB-Indoor-Location-Tracker

Real-time indoor positioning system using Ultra-Wideband (UWB), ESP32, and Python. The system implements Two-Way Ranging (TWR) and trilateration algorithms to estimate and visualize the position of a mobile tracking tag in real time.

---

## Overview

Traditional GPS systems suffer significant accuracy degradation indoors due to signal attenuation and multipath effects. This project demonstrates an indoor tracking solution using Ultra-Wideband (UWB) technology and a three-anchor architecture to achieve high-accuracy localization.

The system consists of:

- 3 Fixed UWB Anchors
- 1 Mobile UWB Tag
- ESP32-S3 + DW3000 UWB hardware
- Python visualization software
- Custom enclosure design
<img width="1045" height="1107" alt="Image (2)" src="https://github.com/user-attachments/assets/cfc13495-5625-4653-baae-b7375379653a" />

---

## Hardware

- ESP32-S3
- Qorvo DW3000 UWB Transceiver
- OLED Display
- LiPo Battery
- USB-C Connectivity

### CAD Design

Front View

<img width="1626" height="1339" alt="Image (4)" src="https://github.com/user-attachments/assets/7fbdb8f2-27fb-4e7e-9e67-0b6fbd053055" />

Rear View

<img width="1626" height="1339" alt="Image (3)" src="https://github.com/user-attachments/assets/a8db6bdf-002b-4d37-a67b-e771ec66a8eb" />

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

          Laptop/Python GUI
