"""
pipeline_convert_MIDI_to_eMBtxt.py

Convert standard MIDI files into text-based musical stimulus files for the
eMusic Box Roma (eMB Roma).

The generated text files are intended to be loaded by the Max/MSP eMB patch.
Each row corresponds to a discretized temporal frame. Notes are encoded as
MIDI-style triplets:

    pitch velocity duration

Multiple triplets can occur in the same row for polyphonic events. Silent
frames are encoded as:

    0 0 0

Metadata rows:
    -3 = number of frames
    -2 = tempo
    -1 = number of beats

Original author:
    Sara F. Abalde

Created:
    6 July 2022

Modification history:
    10 November 2022:
        Added support for multiple note onsets in the same row, allowing
        polyphonic events such as chords in the eMB text files.

Dependencies:
    pretty_midi
    numpy
    matplotlib
    pypianoroll

Installation example:
    conda install -c conda-forge pretty_midi
    pip install pypianoroll matplotlib numpy
"""

from pathlib import Path
import os
import re

import matplotlib.pyplot as plt
import numpy as np
import pretty_midi
import pypianoroll


# -------------------------------------------------------------------------
# User configuration
# -------------------------------------------------------------------------

# Song titles to include when opt_allfolder is False.
midi_titles = [
    "Get down on it",
    "Thriller",
    "We found love",
    "Freed from desire",
]

# Folder containing input MIDI files.
pathmidi = Path(
    "C:/Users/saraf/OneDrive - Fondazione Istituto Italiano Tecnologia/"
    "E-musicbox/MIDIs/MIDI simplified/exp/"
)

# If True, convert all valid MIDI files in pathmidi.
# If False, only convert files starting with one of the names in midi_titles.
opt_allfolder = False

# Folder where eMB text files and optional plots will be saved.
pathout = Path(
    "C:/Users/saraf/OneDrive - Fondazione Istituto Italiano Tecnologia/"
    "E-musicbox/MIDIs/MIDI simplified/"
)

# Output options.
opt_intersp = False
opt_save_txteMB = True
opt_showPlots = True
opt_savePlots = False

# Filename options.
# True if input MIDI files are named using a song-number format,
# for example: song1_inst1-drums.mid
opt_nameinputfiles_songNbr = False

# True to generate output filenames with the "vo_nospac" label.
opt_nameoutfiles_vonospac = False

# If True, bass MIDI files are assumed to already be transposed one octave lower.
opt_simplified_midi = True


# -------------------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------------------

def list_midi_files(input_folder, all_folder=False, titles=None):
    """Return MIDI files to be converted."""
    files = next(os.walk(input_folder))[2]

    excluded_extensions = (".txt", ".tar", ".wav", ".mp3")

    if all_folder:
        return [
            file
            for file in files
            if not file.endswith(excluded_extensions)
        ]

    return [
        file
        for file in files
        if any(file.startswith(title) for title in titles)
        and not file.endswith(excluded_extensions)
    ]


def parse_filename(filename, titles, use_song_number_format=False):
    """
    Extract song and instrument information from the filename.

    Expected default format:
        Song title_instrument.mid

    Example:
        Thriller_bass.mid

    Optional song-number format:
        song1_inst1-drums.mid
    """
    if use_song_number_format:
        song_number = int(re.split(r"(\d+)", filename)[1]) - 1

        file_parts = filename.split(".")[0].split("-")
        file_parts[0] = titles[song_number]

        return file_parts

    filename_without_extension = filename.split(".")
    return filename_without_extension[0].split("_")


def get_output_filename(song_name, instrument_name):
    """Create the output filename according to the selected naming option."""
    if opt_intersp:
        return f"{song_name} _vo_intersp _{instrument_name}.txt"

    if opt_nameinputfiles_songNbr:
        return f"{song_name} _vo_full20bars _{instrument_name}.txt"

    if opt_nameoutfiles_vonospac:
        return f"{song_name} _vo_nospac _{instrument_name}.txt"

    return f"{song_name} _{instrument_name}.txt"


def write_note_triplet(file_handle, pitch, velocity, duration, instrument_name, is_last):
    """
    Write one note triplet to the eMB text file.

    For keys and drums, durations are reduced to avoid excessive overlap
    during fast eMB rotations. For bass, notes can optionally be transposed
    one octave lower when opt_simplified_midi is False.
    """
    if instrument_name == "keys" or instrument_name == "drums":
        note_duration = round(duration / 1.25)
        file_handle.write(f"{pitch} {velocity} {note_duration}")

    elif instrument_name == "bass":
        if opt_simplified_midi:
            file_handle.write(f"{pitch} {velocity} {duration}")
        else:
            file_handle.write(f"{pitch - 12} {velocity} {duration}")

    else:
        file_handle.write(f"{pitch} {velocity} {duration}")

    if is_last:
        file_handle.write(";\n")
    else:
        file_handle.write(" ")


def plot_midi_pianoroll(midi_data, song_name, instrument_name, output_folder):
    """Visualize the MIDI file as a piano roll."""
    piano_roll = pypianoroll.from_pretty_midi(midi_data)

    fig1, ax1 = plt.subplots()

    resolution = 16
    pypianoroll.plot_track(
        piano_roll.tracks[0],
        ax1,
        xtick="beat",
        ytick="octave",
        resolution=resolution,
    )

    # Preserve the original plotting behavior.
    min_pitch = piano_roll.tracks[0].pianoroll.min()
    max_pitch = piano_roll.tracks[0].pianoroll.max()
    ax1.set_ylim(min_pitch, max_pitch)

    num_bars = len(piano_roll.tracks[0].pianoroll)
    bar_labels = [f"Bar {i + 1}" for i in range(num_bars)]
    ax1.set_xticklabels(bar_labels)

    plt.title(f"{song_name}_{instrument_name}")

    if opt_savePlots:
        plot_path = output_folder / f"{song_name}{instrument_name}.pdf"
        plt.savefig(plot_path, format="pdf", bbox_inches="tight")

    plt.show()


# -------------------------------------------------------------------------
# Main conversion pipeline
# -------------------------------------------------------------------------

filenames = list_midi_files(
    input_folder=pathmidi,
    all_folder=opt_allfolder,
    titles=midi_titles,
)

for filename in filenames:
    song_and_instrument = parse_filename(
        filename=filename,
        titles=midi_titles,
        use_song_number_format=opt_nameinputfiles_songNbr,
    )

    song_name = song_and_instrument[0]
    instrument_name = song_and_instrument[1]

    midi_data = pretty_midi.PrettyMIDI(str(pathmidi / filename))

    tempo = round(midi_data.get_tempo_changes()[1][0])
    beats = midi_data.get_beats()
    numBeats = len(beats)

    # Duration is estimated as the last beat plus one inter-beat interval.
    duration = beats[-1] + beats[1]

    # Sixteenth-note grid: 4 temporal frames per beat.
    step = duration / (numBeats * 4)
    frames = np.around(np.arange(0, duration, step), 2)

    pitch = []
    onset = []
    offset = []
    dur = []
    vel = []

    for instrument in midi_data.instruments:
        instrument.name = song_name

        # Mark drum files as drum tracks.
        if instrument_name == "drums":
            instrument.is_drum = True

        print(instrument)

        for note in instrument.notes:
            pitch.append(note.pitch)
            onset.append(round(note.start, 2))
            offset.append("{:.2f}".format(note.end))

            # Increase low velocities to make quiet notes more audible.
            if note.velocity < 50:
                vel.append(note.velocity + 80)
            else:
                vel.append(note.velocity)

            dur.append(round((note.end - note.start) * 1000))

        if opt_showPlots:
            plot_midi_pianoroll(
                midi_data=midi_data,
                song_name=song_name,
                instrument_name=instrument_name,
                output_folder=pathout,
            )

    # ---------------------------------------------------------------------
    # Save eMB text file
    # ---------------------------------------------------------------------

    if opt_save_txteMB:
        output_filename = get_output_filename(song_name, instrument_name)
        output_path = pathout / output_filename

        with open(output_path, "w+", encoding="utf-8") as f:
            # Metadata rows.
            f.write("-3, " + str(len(frames)) + ";\n")
            f.write("-2, " + str(tempo) + ";\n")
            f.write("-1, " + str(numBeats) + ";\n")

            # Create eMB text file with one row per temporal frame.
            for i in range(len(frames)):
                if frames[i] in onset:
                    idx = np.where(onset == frames[i])[0]

                    for i_onset in range(idx.shape[0]):
                        is_first_note = i_onset == 0
                        is_last_note = i_onset == idx.shape[0] - 1

                        if is_first_note:
                            f.write(str(i + 1) + ", ")

                        write_note_triplet(
                            file_handle=f,
                            pitch=pitch[idx[i_onset]],
                            velocity=vel[idx[i_onset]],
                            duration=dur[idx[i_onset]],
                            instrument_name=instrument_name,
                            is_last=is_last_note,
                        )

                else:
                    f.write(str(i + 1) + ",  0  0  0  ;\n")
