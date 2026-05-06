# eMusic Box (eMB) Roma Methodological Paper Code and Data

This repository contains the code, Max/MSP patch resources, supplementary scripts, example data, and experiment configuration files associated with the methodological paper:

> The e-Music Box Roma: An open instrument for accessible music making
> Sara F. Abalde, Félix Bigand, Lorenzo Orciari, Claudio Lorini, Peter E. Keller, Alberto Parmiggiani, Marco Crepaldi, Giacomo Novembre
> [Journal/conference/preprint link here]  
> DOI: [DOI here]

## Repository overview

```text
.
├── src/
│   ├── emb_dual/                  # Code for the eMB dual method/system
│   └── emb_solo/                  # Code for the eMB solo method/system
├── max_msp/
│   └── emb_solo_patch/            # Max/MSP patch and all required folders
│       ├── patchers/              # Main and auxiliary .maxpat files
│       ├── media/                 # Audio/media assets required by the patch
│       ├── externals/             # External Max objects, if redistributable
│       └── docs/                  # Patch-specific notes and screenshots
├── supplementary/
│   └── python/                    # Supplementary Python scripts, e.g. data creation
├── data/
│   ├── midi/                      # Original MIDI files
│   ├── emb_ready/                 # MIDI-like files prepared for eMB
│   └── example_trials/            # Example trial files for testing/reproduction
├── configs/
│   ├── experiments/               # Experiment configuration files
│   └── examples/                  # Minimal example configs
├── docs/                          # Extended documentation
├── scripts/                       # Utility scripts for setup/checks
└── tests/                         # Lightweight tests or validation checks
```

## What is included

| Component | Description |
|---|---|
| `src/emb_dual/` | Implementation of the eMB dual system. |
| `src/emb_solo/` | Implementation of the eMB solo system. |
| `max_msp/emb_solo_patch/` | Max/MSP implementation for eMB solo, including patchers and required subfolders. |
| `supplementary/python/` | Scripts used to generate, transform, or inspect supplementary data. |
| `data/midi/` | Source MIDI files used in the examples or experiments. |
| `data/emb_ready/` | MIDI-like files already converted/prepared for eMB. |
| `data/example_trials/` | Example trials for testing the workflow without running the full experiment. |
| `configs/experiments/` | Experiment configuration files used in the paper. |

## Quick start

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

Run a basic repository check:

```bash
python scripts/check_repository.py
```

Run an example supplementary script:

```bash
python supplementary/python/create_example_emb_ready_file.py \
  --input data/midi/example.mid \
  --output data/emb_ready/example_emb_ready.csv
```

## Using the eMB dual code

The eMB dual code is located in:

```text
src/emb_dual/
```

Recommended workflow:

1. Place or select the relevant input files from `data/midi/` or `data/emb_ready/`.
2. Select an experiment configuration from `configs/experiments/`.
3. Run the main eMB dual script or notebook.
4. Save generated outputs outside the repository or in an ignored `outputs/` directory.

Example command placeholder:

```bash
python -m src.emb_dual.run_dual \
  --config configs/examples/example_dual_config.yaml
```

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
