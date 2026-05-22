# eMB Roma Firmware

This folder contains the Arduino firmware (eMB_firmware.ino) used to operate the eMusic Box Roma after assembly.

The firmware acquires:

- rotary angle data from the AS5047P magnetic rotary encoder,
- linear slider position,
- push button state,

and streams these values in real time to the core computer through a serial USB connection.

---

## Hardware requirements

The firmware was developed for:

- Adafruit Feather M0 microcontroller
- AS5047P magnetic rotary encoder
- Linear slider potentiometer
- Push button

The AS5047P encoder communicates with the microcontroller through SPI.

---

## Dependencies

Install the following Arduino library before compiling:

- AS5047P Arduino library  
  https://github.com/jonas-merkle/AS5047P

---

## Firmware configuration

Two parameters may need to be adjusted for each individual eMB after assembly:

```cpp
float value_offset_zero = 118.0;
RotationDirection rotation_direction = CW;
```

### Zero-position calibration

`value_offset_zero` defines the angular offset corresponding to the desired 0° position of the device.

After assembling the eMB:

1. Upload the firmware.
2. Open the Arduino serial monitor.
3. Rotate the device to the desired zero position.
4. Adjust `value_offset_zero` until the reported angle corresponds to 0°.

This calibration only needs to be performed once unless the encoder or magnet position changes.

---

## Rotation direction

The direction of rotation can be configured as:

```cpp
CW
```

or:

```cpp
CCW
```

Clockwise (`CW`) rotation is the default behavior.

---

## Serial output

The firmware streams ASCII-encoded values through the serial port at 9600 baud in the following format:

```text
slider_value corrected_angle
```

Example:

```text
523 142.31
```

---

## Uploading the firmware

1. Open the `.ino` file in the Arduino IDE.
2. Select the correct board and COM port.
3. Compile and upload the firmware.
4. Close the Arduino serial monitor before starting the Max/MSP patch so the serial port becomes available.

---

## Related software

The streamed serial data are used by the Max/MSP control patches located in:

```text
software/max_msp/
```

These patches handle:

- real-time acquisition,
- musical event mapping,
- MIDI playback,
- synchronization,
- and experimental control.
