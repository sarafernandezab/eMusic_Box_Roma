# eMusic Box Roma (eMB Roma)

This repository contains the open-source hardware files, firmware, Max/MSP control patches, musical stimuli, configuration files, and supplementary Python scripts associated with the methodological paper:

> *The e-Music Box Roma: An open instrument for accessible music making*  
> Sara F. Abalde, Félix Bigand, Lorenzo Orciari, Claudio Lorini, Peter E. Keller, Alberto Parmiggiani, Marco Crepaldi, Giacomo Novembre  
> [Journal/conference/preprint link here]  
> DOI: [DOI here]

The eMusic Box Roma (eMB Roma) is an open instrument for accessible music making. It combines a 3D-printed rotary interface, embedded electronics, custom firmware, and Max/MSP software for interactive musical stimulus presentation and experimental control. The system supports both solo and dual use.

---

## Repository structure

```text
.
├── hardware/
│   └── stl/
│       ├── rotary_disk_group/
│       ├── cover_group/
│       ├── base_group/
│       └── README.md
│
├── firmware/
│   └── emb_firmware/
│
├── software/
│   └── max_msp/
│       ├── emb_solo/
│       └── emb_dual/
│
├── musical_stimuli/
│   ├── midi/
│   ├── midi_derived_text/
│   └── conversion_scripts/
│
├── configs/
│   ├── global/
│   └── experiments/
│
├── supplementary/
│   ├── config_generation/
│   ├── utilities/
│   └── analysis/
│
├── docs/
├── scripts/
├── tests/
├── requirements.txt
└── README.md
```

---

## Hardware design and construction

The `hardware/stl/` folder contains the open-source STL files required to fabricate the eMB Roma enclosure and mechanical components.

The mechanical design is organized according to the three main structural groups described in the paper:

| Folder | Description |
|---|---|
| `hardware/stl/rotary_disk_group/` | STL files for the rotary disk assembly, including the disk that supports the rotating handle. |
| `hardware/stl/cover_group/` | STL files for the cover group, including components that support the bearing and disk alignment. |
| `hardware/stl/base_group/` | STL files for the base group, including placeholders for the microcontroller, magnetic rotary encoder, USB connector, and feet. |
| `hardware/stl/README.md` | Printing and assembly notes for fabricating the eMB Roma. |

The STL files correspond to the printable components of the eMB Roma. In the implementation described in the paper, parts were printed in Nylon PA 6-6, although other materials may be used depending on experimental or fabrication constraints.

Additional non-printed mechanical components include the rotating handle, ball bearing, ferrite ring, and self-tapping screws. Assembly details, screw sizes, and component placement should be documented in `hardware/stl/README.md`.

---

## Electronic architecture

The eMB Roma integrates:

- a magnetic rotary encoder for measuring disk rotation,
- a linear slider,
- a push button,
- and a microcontroller for data acquisition and USB communication.

The firmware and software assume that all input signals are streamed from the microcontroller to the core computer through a serial connection over USB.

Hardware-specific wiring diagrams, component lists, and assembly notes can be placed in `docs/`.

---

## Firmware and data communication

The firmware is located in:

```text
firmware/emb_firmware/
```

The firmware is uploaded to the microcontroller during initial device setup. During routine use, it reads:

- rotary angle from the magnetic rotary encoder,
- slider position from the linear potentiometer,
- push button state from the digital input.

These values are streamed to the core computer through a serial COM port using ASCII-encoded messages.

The firmware includes device-specific calibration parameters. In particular, the angular zero position can be adjusted using the `value_offset_zero` parameter. This corrects for small differences in encoder and magnet alignment after assembly.

The direction of rotation can also be configured in the firmware. By default, the eMB Roma is set to clockwise rotation. This can be inverted by changing the `rotation_direction` parameter from `CW` to `CCW`. After changing the rotation direction, the zero-reference parameter may need to be verified or adjusted.

Once the firmware has been uploaded and calibration is complete, the Arduino environment should be closed so that the serial port is available to the Max/MSP control patch.

---

## Software architecture and experimental control

The Max/MSP software is located in:

```text
software/max_msp/
```

Two ready-to-use Max/MSP projects are provided:

| Folder | Description |
|---|---|
| `software/max_msp/emb_solo/` | Max/MSP patch for solo eMB use. |
| `software/max_msp/emb_dual/` | Max/MSP patch for dual eMB use. |

The Max/MSP patch provides a graphical interface for:

- loading configuration files,
- selecting musical stimuli,
- assigning instruments to eMB devices,
- receiving serial data from the eMB,
- mapping rotational position to musical events,
- playing MIDI output streams,
- logging behavioral and musical data,
- and sending optional synchronization triggers to external systems.

---

## Configuration files

Configuration files are located in:

```text
configs/
```

The software uses two main types of configuration files:

| Folder | Description |
|---|---|
| `configs/global/` | Global configuration files containing setup-wide parameters such as COM ports, sampling rate, stimulus paths, output paths, instrument assignments, metronome settings, and optional trigger settings. |
| `configs/experiments/` | Trial-specific experiment configuration files, with one row per trial. These files define parameters such as trial number, condition, song, number of bars, instrument assignment, metronome tempo, and number of metronome beats. |

Configuration files are plain-text files and can be generated automatically using the supplementary Python scripts.

---

## Musical stimuli

Musical stimuli are located in:

```text
musical_stimuli/
```

The eMB Roma uses MIDI-derived text files that can be read by the Max/MSP patch and synchronized with the rotational position of the device.

| Folder | Description |
|---|---|
| `musical_stimuli/midi/` | Original MIDI files. |
| `musical_stimuli/midi_derived_text/` | Text-based MIDI-derived stimulus files used by the Max/MSP patch. |
| `musical_stimuli/conversion_scripts/` | Python scripts for converting MIDI files into eMB-compatible text files. |

By default, one full rotation of the eMB corresponds to one musical bar divided into 16 equally spaced steps, matching the sixteenth-note structure of a 4/4 bar. Each row of a MIDI-derived text file represents a discrete temporal frame. Notes are encoded using MIDI-style values such as pitch, velocity, and duration.

Polyphonic stimuli are supported by including multiple note triplets in the same temporal frame. Frames without musical events are represented as silence.

The conversion scripts support batch conversion of MIDI files and can extract metadata such as tempo and bar count. If a MIDI file contains multiple instruments, the instrumental parts should be separated before conversion, with filenames indicating the corresponding instrument.

---

## Supplementary Python scripts

Supplementary scripts are located in:

```text
supplementary/
```

These scripts support reproducible preparation of files used by the eMB Roma system.

| Folder | Description |
|---|---|
| `supplementary/config_generation/` | Python scripts for generating global and experiment configuration files. |
| `supplementary/utilities/` | Additional utility scripts for preparing or checking repository resources. |
| `supplementary/analysis/` | Optional scripts for inspecting or analyzing output files. |

Example:

```bash
python supplementary/config_generation/create_configs.py
```

---

## Trial execution and data output

During a trial, the Max/MSP patch receives the continuous angular position of each eMB and discretizes it into temporal bins. The discretized within-bar position is combined with the completed rotation count to determine the absolute position in the musical sequence. This absolute position is then used to trigger the corresponding MIDI-derived musical event.

For each completed trial, the Max/MSP patch can save:

1. a raw text data file containing timestamped eMB data,
2. a MIDI file containing the musical output streams,
3. and, when enabled, a summary log file.

The raw text data file contains the main behavioral data used for analysis, including angular position, discretized musical position, rotation cycle count, and instrument information for each connected eMB.

---

## Synchronization with external devices

The Max/MSP patch can optionally send synchronization triggers through COM ports. These triggers can mark events such as trial onset, trial offset, or predefined rhythmic positions.

This feature is intended for synchronization with external recording systems such as EEG, motion capture, or other multimodal acquisition devices.

---

## Example use cases

The eMB Roma supports different experimental and musical configurations along two main dimensions:

1. **Musical complexity**  
   The system can be configured for monophonic or polyphonic playback, single or multiple instruments, identical or complementary musical streams, and optional real-time parameter modulation through the linear slider.

2. **Social configuration**  
   The system supports solo use with one eMB and dual use with two eMBs. The repository provides separate Max/MSP patches for these two validated configurations.

Example dual-use configurations include:

- **Unison duet**: both eMBs play the same instrument and musical sequence.
- **Counterpoint duet**: the eMBs play different but complementary musical lines.
- **Band-like duet**: one eMB controls melodic streams while the other controls rhythmic or harmonic streams.

Multi-user setups beyond two devices may be possible with additional software and synchronization development, but they are not included as ready-to-use configurations in this repository.

---

## Quick start

Clone the repository:

```bash
git clone https://github.com/sarafernandezab/eMusic_Box_Roma.git
cd eMusic_Box_Roma
```

Create a Python environment:

```bash
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
# .venv\Scripts\activate       # Windows

pip install -r requirements.txt
```

Upload the firmware to the microcontroller using the Arduino environment.

Then open the appropriate Max/MSP project:

```text
software/max_msp/emb_solo/
```

or:

```text
software/max_msp/emb_dual/
```

Load the global and experiment configuration files from `configs/`, then select the desired musical stimuli from `musical_stimuli/midi_derived_text/`.

---

## Dependencies

The repository may require:

- Arduino IDE or compatible Arduino development environment,
- AS5047P Arduino library,
- Max 8 or later,
- Python 3,
- Python libraries listed in `requirements.txt`.

---

## Citation

If you use this repository, please cite:

```bibtex
@article{emb_roma,
  title={The e-Music Box Roma: An open instrument for accessible music making},
  author={Abalde, Sara F. and Bigand, Félix and Orciari, Lorenzo and others},
  journal={...},
  year={2026}
}
```
