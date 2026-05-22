# eMusic Box (eMB) Roma — Repository

This repository contains the firmware, software, printable hardware files, musical stimuli, supplementary scripts, and configuration resources associated with the methodological paper:

> *The e-Music Box Roma: An open instrument for accessible music making*  
> Sara F. Abalde, Félix Bigand, Lorenzo Orciari, Claudio Lorini, Peter E. Keller, Alberto Parmiggiani, Marco Crepaldi, Giacomo Novembre  
> [Journal/conference/preprint link here]  
> DOI: [DOI here]

---

# Repository Overview

```text
.
├── hardware/
│   └── stl/
│       ├── enclosure/
│       ├── gears/
│       └── README.md                 # Printing instructions for the eMB
│
├── firmware/
│   ├── emb_solo/
│   └── emb_dual/
│
├── software/
│   ├── max_msp/
│   │   ├── emb_solo/
│   │   │   ├── patchers/
│   │   │   ├── media/
│   │   │   ├── externals/
│   │   │   └── docs/
│   │   │
│   │   └── emb_dual/
│   │       ├── patchers/
│   │       ├── media/
│   │       ├── externals/
│   │       └── docs/
│   │
│   └── python/
│       ├── emb_solo/
│       └── emb_dual/
│
├── musical_stimuli/
│   ├── midi/                         # Original MIDI files
│   ├── text_converted_midis/         # MIDI-like converted text formats for eMB
│   └── conversion_scripts/
│       └── midi_conversion_tools.py
│
├── supplementary/
│   ├── config_generation/
│   │   └── create_configs.py
│   ├── utilities/
│   └── analysis/
│
├── configs/
│   ├── experiments/
│   └── examples/
│
├── docs/
│
├── scripts/
│
├── tests/
│
├── requirements.txt
└── README.md
```

---

# Repository Components

| Folder | Description |
|---|---|
| `hardware/stl/` | STL files for 3D printing the eMusic Box (eMB) hardware components. |
| `firmware/` | Firmware for operating the eMB hardware in solo or dual configurations. |
| `software/max_msp/` | Max/MSP projects for running the eMB in solo or dual interaction modes. |
| `software/python/` | Python-based implementations or support scripts for eMB operation. |
| `musical_stimuli/midi/` | Original MIDI files used in experiments and demonstrations. |
| `musical_stimuli/text_converted_midis/` | MIDI files converted into text-based formats compatible with the eMB workflow. |
| `musical_stimuli/conversion_scripts/` | Python scripts used to convert MIDI files into eMB-compatible formats. |
| `supplementary/config_generation/` | Scripts used to automatically generate experiment configuration files. |
| `supplementary/utilities/` | Additional utility scripts supporting repository workflows. |
| `configs/` | Example and experiment configuration files. |
| `docs/` | Extended documentation, screenshots, diagrams, and setup notes. |

---

# 3D Printing the eMB

The STL files required to print the eMusic Box (eMB) are located in:

```text
hardware/stl/
```

These files contain the printable mechanical components of the instrument, including enclosure parts and mechanical transmission elements.

Printing recommendations, assembly notes, and hardware-specific instructions can be included in:

```text
hardware/stl/README.md
```

---

# Firmware

The firmware source code is located in:

```text
firmware/
```

Separate folders are provided for:

- `emb_solo/` — solo interaction mode
- `emb_dual/` — dual interaction mode

## Firmware Notes

> The direction of rotation (clockwise or counterclockwise) can be configured in the firmware. By default, the eMB is set to clockwise rotation.

---

# Software

The software resources are located in:

```text
software/
```

Two software approaches can be included:

## Max/MSP

Located in:

```text
software/max_msp/
```

Includes:

- Max/MSP patches
- media assets
- external objects
- patch documentation

Separate projects can be maintained for:

- solo performance
- dual performance

## Python

Located in:

```text
software/python/
```

Optional Python implementations or support tools for the eMB system.

---

# Musical Stimuli

The musical stimuli resources are located in:

```text
musical_stimuli/
```

This section contains:

- original MIDI stimuli
- text-converted MIDI representations
- scripts used for conversion and preprocessing

Example structure:

```text
musical_stimuli/
├── midi/
├── text_converted_midis/
└── conversion_scripts/
```

---

# Supplementary Scripts

Supplementary scripts are located in:

```text
supplementary/
```

These include:

- configuration generation tools
- utility scripts
- analysis scripts

Example:

```bash
python supplementary/config_generation/create_configs.py
```

---

# Quick Start

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
cd YOUR-REPOSITORY
```

Create a Python environment:

```bash
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
# .venv\Scripts\activate       # Windows

pip install -r requirements.txt
```

Run a repository check:

```bash
python scripts/check_repository.py
```

---

# Citation

If you use this repository, please cite:

```bibtex
@article{emb_roma,
  title={The e-Music Box Roma: An open instrument for accessible music making},
  author={Abalde, Sara F. and Bigand, Félix and Orciari, Lorenzo and others},
  journal={...},
  year={2026}
}
```required, rotation direction can be inverted by changing the \code{rotation\_direction} parameter from \code{CW} to \code{CCW}. 


This inverts the computed angle in firmware after applying the device offset but before streaming. Practically, this can be implemented by computing the aligned angle in the 0--360° range (for example \code{angle = fmod(readAngleDegree() - value\_offset\_zero + 360.0, 360.0)} and then replacing the streamed value with its mirror angle (\code{angle = fmod(360.0 - angle + 360.0, 360.0)}) when counter-clockwise behavior is required. After changing the mapping, the zero reference (\code{value\_offset\_zero}) needs to be verified or updated accordingly per device so remains correct.**

## Using the eMB solo code

The eMB solo code is located in:

```text
src/emb_solo/
```

Example command placeholder:

```bash
python -m src.emb_solo.run_solo \
  --config configs/examples/example_solo_config.yaml
```

## Using the Max/MSP eMB solo patch

The Max/MSP patch is located in:

```text
max_msp/emb_solo_patch/
```

Suggested organization:

```text
max_msp/emb_solo_patch/
├── patchers/      # Main .maxpat patch and abstractions
├── media/         # Required sound/media files
├── externals/     # External dependencies, if license permits redistribution
└── docs/          # Patch-specific documentation
```

To use the patch:

1. Open Max/MSP.
2. Add `max_msp/emb_solo_patch/` to the Max file path.
3. Open the main patch in `max_msp/emb_solo_patch/patchers/`.
4. Check the dependency notes in `max_msp/emb_solo_patch/docs/MAX_MSP_PATCH_NOTES.md`.
5. Load one of the example trial/configuration files from `data/example_trials/` or `configs/examples/`.

If external objects are required but cannot be redistributed, list them in `max_msp/emb_solo_patch/docs/MAX_MSP_PATCH_NOTES.md` with installation links or package names.

## Data

The repository separates original and derived data:

```text
data/midi/          # Original MIDI files
data/emb_ready/     # Prepared MIDI-like files for eMB
data/example_trials/# Example trial data
```

Large data files should not be committed directly to GitHub. For large datasets, use one of the following:

- Git LFS
- Zenodo, OSF, Figshare, or institutional repository
- A release asset attached to the GitHub repository

Document large external files in `data/README.md`.

## Reproducing paper examples

A minimal reproduction workflow should use:

```text
configs/examples/
data/example_trials/
supplementary/python/
```

Recommended command placeholder:

```bash
python supplementary/python/create_example_emb_ready_file.py \
  --input data/midi/example.mid \
  --output data/emb_ready/example_emb_ready.csv
```

## Citation

If you use this repository, please cite the paper and this code repository.

See [`CITATION.cff`](CITATION.cff).

## License

Code license: see [`LICENSE`](LICENSE).  
Data license: specify in [`data/README.md`](data/README.md).

## Contact

For questions, contact:

- [Name]
- [Email]
- [Institution]
