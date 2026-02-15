# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

muviz is a Python CLI tool that converts audio files into abstract art-style MP4 visualization videos. It analyzes audio features (FFT spectrum, RMS energy, frequency bands) and renders them as animated visuals.

## Development Environment

The project uses a virtual environment created with `uv`:
```bash
uv venv .venv
source .venv/Scripts/activate  # Windows
# or source .venv/bin/activate  # Unix
uv pip install -r requirements.txt
```

## Running the Tool

```bash
# Activate venv first
source .venv/Scripts/activate

# Basic usage
python -m muviz.cli input.wav -o output.mp4

# With custom options
python -m muviz.cli input.mp3 -o video.mp4 --style particle --theme neon --duration 30
```

## Architecture

The project follows a pipeline architecture:
1. **CLI** (`cli.py`) - Entry point using Click framework, parses arguments and orchestrates the flow
2. **Audio Analysis** (`audio/analyzer.py`) - Uses librosa to extract FFT spectrum, RMS energy, frequency bands
3. **Visualization** (`visualizer/`) - Abstract base class + 3 implementations:
   - `geometric.py`: Concentric circles and rotating polygons
   - `particle.py`: Particle system reacting to audio energy
   - `abstract.py`: Flowing waveforms and frequency bars
4. **Rendering** (`renderer/`) - Frame generation and video writing with MoviePy

## Key Patterns

- `VisualizerConfig` dataclass holds all visualization settings (width, height, fps, style, theme)
- Themes are defined in `config/settings.py` as dictionaries with background and frequency band colors
- Visualizers receive audio_data dict: `{"rms": float, "spectrum": np.ndarray, "waveform": np.ndarray, "frequency_bands": (low, mid, high)}`
- MoviePy 2.x API uses `with_audio()` instead of `set_audio()` and removed the `verbose` parameter

## Common Development Tasks

```bash
# Test with short duration
python -m muviz.cli test.wav -o out.mp4 --duration 3

# Test different styles
python -m muviz.cli test.wav -o geo.mp4 --style geometric
python -m muviz.cli test.wav -o part.mp4 --style particle
python -m muviz.cli test.wav -o abst.mp4 --style abstract
```
