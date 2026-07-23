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

---

## Hardware

- ESP32-S3
- Qorvo DW3000 UWB Transceiver
- OLED Display
- LiPo Battery
- USB-C Connectivity

### CAD Design

Front View

(Add CAD Front Render Here)

Rear View

(Add CAD Rear Render Here)

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
