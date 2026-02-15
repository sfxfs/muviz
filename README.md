# muviz

将一段音频文件可视化为视频 | Visualize audio files as a video.

## Installation

```bash
pip install -e .
```

## Usage

```bash
# Basic usage
muviz input.wav -o output.mp4

# Advanced usage
muviz input.mp3 -o video.mp4 \
    --style geometric \
    --width 1920 \
    --height 1080 \
    --fps 30 \
    --theme cosmic \
    --duration 0
```

## Options

- `input_file`: Path to audio file (wav, mp3, ogg, etc.)
- `-o, --output`: Output video file path
- `--style`: Visualization style (geometric, particle, abstract)
- `--width`: Video width (default: 1920)
- `--height`: Video height (default: 1080)
- `--fps`: Frames per second (default: 30)
- `--theme`: Color theme (cosmic, neon, pastel)
- `--duration`: Duration in seconds (0 for full audio)

## Features

- Multiple visualization styles:
  - **geometric**: Concentric circles and polygons
  - **particle**: Particle system effects
  - **abstract**: Flowing waveforms and frequency bars
- Multiple color themes:
  - **cosmic**: Deep space colors
  - **neon**: Bright neon colors
  - **pastel**: Soft pastel colors
- High-quality video output with audio
