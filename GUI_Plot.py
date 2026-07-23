import math
import re
import time
from collections import deque
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import serial

import serial.tools.list_ports
# =========================================================
# CONFIG
# =========================================================
# Anchor positions in centimeters
# Example layout for a ~20 ft x 20 ft room (~610 cm x 610 cm)
A0X, A0Y = 0, 0
A1X, A1Y = 610, 0
A2X, A2Y = 0, 610
ANCHORS = {
0: (A0X, A0Y),
1: (A1X, A1Y),
2: (A2X, A2Y),
}
SERIAL_BAUD = 115200
SERIAL_TIMEOUT = 0.05
# Set to a COM port like "COM7" if you want to force one.
# Leave as None to auto-pick the first detected serial port.
FORCE_COM_PORT = None
# Optional smoothing. Higher = smoother but more lag.
SMOOTHING_ALPHA = 0.25
# Number of past positions to show
TRAIL_LENGTH = 40
# =========================================================
# SERIAL HELPERS
# =========================================================
def get_first_com():
ports = list(serial.tools.list_ports.comports())
if not ports:
return None
print("Detected serial ports:")
for p in ports:
print(f" {p.device} - {p.description}")
return ports[0].device
def open_serial():

port = FORCE_COM_PORT if FORCE_COM_PORT else get_first_com()
if port is None:
raise RuntimeError("No serial port found.")
print(f"Opening serial port: {port}")
ser = serial.Serial(port, SERIAL_BAUD, timeout=SERIAL_TIMEOUT)
time.sleep(1.0)
return ser
# =========================================================
# PARSING
# =========================================================
def parse_range_line(line):
"""
Parses lines like:
AT+RANGE=tid:0,mask:07,seq:85,range:(504,319,505,0,0,0,0,0),ancid:(0,1,2,-1,-1
,-1,-1,-1)
Returns:
{
"tid": 0,
"ranges": [504,319,505,0,0,0,0,0],
"ancids": [0,1,2,-1,-1,-1,-1,-1]
}
or None if line does not match.
"""
pattern = r"tid:(\d+).*?range:\(([^)]*)\).*?ancid:\(([^)]*)\)"
match = re.search(pattern, line)
if not match:
return None
tid = int(match.group(1))
ranges = [int(x.strip()) for x in match.group(2).split(",")]
ancids = [int(x.strip()) for x in match.group(3).split(",")]
return {
"tid": tid,
"ranges": ranges,
"ancids": ancids,
}
# =========================================================
# MATH
# =========================================================

def trilaterate_3_anchors(p1, r1, p2, r2, p3, r3):
"""
Linearized 2D trilateration.
p1, p2, p3 are (x, y) in cm
r1, r2, r3 are distances in cm
Returns (x, y) or None
"""
x1, y1 = p1
x2, y2 = p2
x3, y3 = p3
A = 2 * (x2 - x1)
B = 2 * (y2 - y1)
C = r1**2 - r2**2 - x1**2 + x2**2 - y1**2 + y2**2
D = 2 * (x3 - x1)
E = 2 * (y3 - y1)
F = r1**2 - r3**2 - x1**2 + x3**2 - y1**2 + y3**2
denom = A * E - B * D
if abs(denom) < 1e-9:
return None
x = (C * E - B * F) / denom
y = (A * F - C * D) / denom
return x, y
def compute_tag_position(parsed):
"""
Uses the first 3 valid anchors from parsed Makerfabs line.
"""
valid = []
for rng, aid in zip(parsed["ranges"], parsed["ancids"]):
if aid in ANCHORS and rng > 0:
valid.append((aid, rng))
if len(valid) < 3:
return None
valid = valid[:3]
(aid1, r1), (aid2, r2), (aid3, r3) = valid
p1 = ANCHORS[aid1]
p2 = ANCHORS[aid2]
p3 = ANCHORS[aid3]
return trilaterate_3_anchors(p1, r1, p2, r2, p3, r3)

def exp_smooth(prev, new, alpha):
if prev is None:
return new
x = alpha * new[0] + (1 - alpha) * prev[0]
y = alpha * new[1] + (1 - alpha) * prev[1]
return x, y
# =========================================================
# STATE
# =========================================================
ser = None
current_raw_position = None
current_smooth_position = None
trail = deque(maxlen=TRAIL_LENGTH)
last_ranges = {0: None, 1: None, 2: None}
# =========================================================
# PLOT SETUP
# =========================================================
fig, ax = plt.subplots(figsize=(8, 8))
anchor_scatter = None
tag_scatter = None
trail_line = None
range_text = None
tag_text = None
def setup_plot():
global anchor_scatter, tag_scatter, trail_line, range_text, tag_text
ax.clear()
anchor_x = [ANCHORS[i][0] for i in sorted(ANCHORS)]
anchor_y = [ANCHORS[i][1] for i in sorted(ANCHORS)]
pad = 80
min_x = min(anchor_x) - pad
max_x = max(anchor_x) + pad
min_y = min(anchor_y) - pad
max_y = max(anchor_y) + pad
# Make square view
span = max(max_x - min_x, max_y - min_y)

cx = (min_x + max_x) / 2
cy = (min_y + max_y) / 2
half = span / 2
ax.set_xlim(cx - half, cx + half)
ax.set_ylim(cy - half, cy + half)
ax.set_title("UWB Tag Position (3 Anchors, 1 Tag)")
ax.set_xlabel("X (cm)")
ax.set_ylabel("Y (cm)")
ax.grid(True)
ax.set_aspect("equal", adjustable="box")
anchor_scatter = ax.scatter(anchor_x, anchor_y, s=100, marker="s",
label="Anchors")
tag_scatter = ax.scatter([], [], s=100, marker="o", label="Tag")
trail_line, = ax.plot([], [], linewidth=1)
for aid, (x, y) in ANCHORS.items():
ax.text(x + 8, y + 8, f"A{aid} ({x}, {y})", fontsize=10)
range_text = ax.text(
0.02, 0.98, "", transform=ax.transAxes, va="top", fontsize=10,
bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
)
tag_text = ax.text(
0.02, 0.88, "", transform=ax.transAxes, va="top", fontsize=10,
bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
)
ax.legend(loc="lower right")
# =========================================================
# UPDATE LOOP
# =========================================================
def read_serial_data():
global current_raw_position, current_smooth_position, trail, last_ranges
if ser is None:
return
# Read a few lines each animation frame to keep display responsive
for _ in range(10):
try:
line = ser.readline().decode("utf-8", errors="ignore").strip()
except Exception as e:

print(f"Serial read error: {e}")
return
if not line:
return
print(line)
parsed = parse_range_line(line)
if parsed is None:
continue
if parsed["tid"] != 0:
continue
for rng, aid in zip(parsed["ranges"], parsed["ancids"]):
if aid in ANCHORS and rng > 0:
last_ranges[aid] = rng
pos = compute_tag_position(parsed)
if pos is None:
continue
current_raw_position = pos
current_smooth_position = exp_smooth(current_smooth_position, pos,
SMOOTHING_ALPHA)
trail.append(current_smooth_position)
def update(frame):
global tag_scatter, trail_line, range_text, tag_text
read_serial_data()
if current_smooth_position is not None:
x, y = current_smooth_position
tag_scatter.set_offsets([[x, y]])
tag_text.set_text(f"Tag: ({x:.1f}, {y:.1f}) cm")
else:
tag_scatter.set_offsets([])
tag_text.set_text("Tag: no fix")
if trail:
xs = [p[0] for p in trail]
ys = [p[1] for p in trail]
trail_line.set_data(xs, ys)
else:
trail_line.set_data([], [])

range_text.set_text(
"Ranges (cm):\n"
f"A0: {last_ranges[0]}\n"
f"A1: {last_ranges[1]}\n"
f"A2: {last_ranges[2]}"
)
return tag_scatter, trail_line, range_text, tag_text
# =========================================================
# MAIN
# =========================================================
def main():
global ser
ser = open_serial()
setup_plot()
ani = FuncAnimation(fig, update, interval=100, cache_frame_data=False)
try:
plt.show()
finally:
if ser is not None and ser.is_open:
ser.close()
print("Serial port closed.")
if __name__ == "__main__":
main()
