# Alarm System Hardware Notes and Maintenance Log

This document records the hardware wiring, power requirements, troubleshooting steps, and project updates for the alarm system based on the Raspberry Pi and multiple sensors.

---

## 1. Overview

This project uses:

- UART version of the MLX90640 thermal camera
- LD2420 or LD2402G millimeter-wave radar sensor
- OLED display
- RGB LED status indicator
- MQTT communication between Raspberry Pi devices
- Scheduled shutdown logic and Wi-Fi monitoring

---

## 2. Raspberry Pi UART Configuration

The UART version of the MLX90640 requires enabling UART4.

Edit the file:

`/boot/firmware/config.txt`

Add the following line:

```ini
dtoverlay=uart4
```

---

## 3. Raspberry Pi 4B Power and GPIO Limits

Important notes:

- A single GPIO pin on Raspberry Pi 4B is typically recommended at around 3 mA, with a maximum limit of 16 mA.
- The total current of all GPIO pins should not exceed 272 mA.
- The 5V header is connected to the power input rail and USB power rail; the recommended current should not exceed 1.5 A.
- For stable operation, sensors and display modules should be powered from a properly rated 5V source with enough current margin.

---

## 4. Wiring Connections

### 4.1 Radar Sensor

Model: LD2420 / LD2402G

| Signal | Pin |
| --- | --- |
| VCC | PIN 2 (5V) |
| GND | PIN 9 |
| OT2 | PIN 13 (GPIO27) |

Notes:

- Detection range is approximately 0.75 m per detection zone.
- LD2420 only supports 3.3V input.
- Average operating current is about 50 mA.
- When powered by 5V, the current must remain within safe operating limits.

### 4.2 Thermal Camera

Model: MLX90640 (UART version)

| Signal | Pin |
| --- | --- |
| VCC | PIN 2 (5V) |
| GND | PIN 14 |
| TX | PIN 24 |
| RX | PIN 21 |

Notes:

- Thermal camera operating current is about 42 mA.
- The 5V rail can provide up to 3 A.
- Max power: 15 W (5V @ 3A)
- Adapter output: DC 5V, up to 3A

### 4.3 OLED Display

| Signal | Pin |
| --- | --- |
| VCC | PIN 4 (5V) |
| GND | PIN 6 |
| SCL | PIN 5 |
| SDA | PIN 3 |

Notes:

- Average current is about 10 mA.
- Reference: Adafruit monochrome OLED breakout documentation.

### 4.4 RGB LED Indicator

| Signal | Pin |
| --- | --- |
| GND | PIN 34 |
| R | PIN 35 (GPIO19) |

Indicator behavior:

- Pulse: program is running normally
- Blink: high-temperature detected

Important note:

- A digital signal-controlled LED module (VCC, GND, S) is recommended.
- A GPIO-driven LED (GPIO, GND) can consume a large amount of current and may require several hundred milliamps.

---

## 5. Power and Stability Notes

### 5.1 Power Cycling Issue

There were cases where the power socket was turned on, but the Raspberry Pi shut down again shortly after startup.

This may be caused by:

- unstable power supply
- startup voltage dips
- current spikes from connected peripherals

### 5.2 Radar Sensor False Detection

The LD2420 millimeter-wave radar sensor began showing abnormal behavior, producing unstable high/low signals and falsely detecting motion even when no person was moving.

The module draws about 50 mA on average and is intended for 3.3V operation. The false detection may be caused by insufficient power quality or unstable input voltage.

After moving the thermal camera to the 5V rail, false detections temporarily stopped.

### 5.3 LD2402G Power Problem

On 2025-04-25, the system was found to output a continuous high level in the morning. After measurement, the input voltage was 5.1V, slightly below the expected 5.3V.

This issue had appeared before and may occur once every few weeks.

Action taken:

- Replaced the LD2402G cable
- Switched to a softer Dupont jumper wire
- Continued monitoring for signs of instability

---

## 6. Software and Runtime Notes

### 6.1 IP Display

Added IP display support.

Install:

```bash
pip install netifaces --break-system-packages
```

### 6.2 Time Synchronization and Shutdown Logic

After a Raspberry Pi reboot, the system keeps the previous time until it synchronizes with the network. The shutdown command is not issued until time synchronization has completed.

The old `rc.local` shutdown logic was removed, and the shutdown timing is managed inside the application code.

### 6.3 Wi-Fi Stability

To inspect Wi-Fi service logs:

```bash
journalctl -u wpa_supplicant.service
```

The system sometimes experiences Wi-Fi dropouts, and signal quality can become poor.

Check signal quality:

```bash
sudo iwlist wlan0 scan | grep -E "SSID|Quality"
```

Observed signal quality was around `-70 dBm`, which indicates a relatively weak connection.

To improve stability:

- Add an older router as a repeater or range extender
- Create a new SSID without underscores in the name

### 6.4 MQTT Setup

A second Raspberry Pi was added in the living room with a speaker to ensure the alarm sound is audible there as well. The Pi was assigned a fixed IP, and a local MQTT broker was configured for communication.

Install the broker:

```bash
sudo apt install mosquitto mosquitto-clients
```

Modify `/etc/mosquitto/mosquitto.conf` and add:

```ini
listener 1883 0.0.0.0
```

Important note:

- `on_connect()` is not called unless the client invokes `loop_start()` (asynchronous) or `loop_forever()` (blocking).
- This is required to handle network traffic and trigger callbacks correctly.

Install scheduling support:

```bash
pip install schedule
```

In this environment, Python `schedule` did not behave reliably, so a loop-based approach was used instead:

```python
schedule.run_pending()
```

---

## 7. MQTT Debugging and Behavior

During testing, messages were still received after restarting or power cycling the devices. This was traced to `clean_session=False`.

Observed behavior:

- When a device reconnects after disconnecting, previously published messages may be received again.
- This is not desirable for our alarm logic.

Solution:

- Use `clean_session=True` so old messages are not replayed after reconnect.

To confirm whether a message is retained, print:

```python
print(f"retain={msg.retain}")
```

---

## 8. Change Log

### 2025-02-15

- Added RGB LED status indication
- Verified that the LED was consuming excessive power when driven directly by GPIO
- Recommended replacing it with a digital signal-controlled LED module

### 2025-02-19

- Replaced the RGB LED with an I2C OLED display
- Average current draw is about 10 mA
- Reference: https://learn.adafruit.com/monochrome-oled-breakouts

### 2025-02-25

- Added IP display support
- Installed:

```bash
pip install netifaces --break-system-packages
```

- Moved shutdown timing into application code rather than relying on `rc.local`

### 2025-03-09

- Purchased a 5V-powered LD2402G sensor
- Shared the 5V output on PIN 2 with the thermal camera

### 2025-04-25

- The LD2402G output stayed high continuously after boot
- Measured input voltage was 5.1V, slightly below 5.3V
- Replaced the sensor cable with a softer Dupont wire and continued monitoring

### 2025-06-02

- Added average temperature display on the OLED so sensor status can be checked in real time

### 2025-07-13

- Added a second Raspberry Pi with a speaker in the living room to improve alarm audibility
- Set fixed IP addresses for the Raspberry Pi devices
- Started a local MQTT broker and used MQTT for communication

### 2025-08-16

- When the kitchen Pi was powered on while the living room Pi was off, MQTT still received messages from the previous session
- Root cause: `clean_session=False`
- Changed to `clean_session=True`
- Confirmed retained message handling by printing `msg.retain`

---

## 9. Summary

This project relies on a combination of:

- a millimeter-wave radar sensor,
- a thermal camera,
- an OLED display,
- and MQTT-based control and monitoring.

The main issues encountered were:

- unstable power delivery,
- false radar detections,
- Wi-Fi instability,
- and MQTT message replay due to session settings.

These were addressed through hardware rewiring, improved power management, logic adjustments, and more careful sensor and communication configuration.

---

End of document.




