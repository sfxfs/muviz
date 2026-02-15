"""Command-line interface for muviz"""

import click
import sys
from pathlib import Path

from muviz.config.settings import VisualizerConfig


@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option(
    "-o", "--output",
    type=click.Path(),
    default=None,
    help="Output video file path"
)
@click.option(
    "--style",
    type=click.Choice(["geometric", "particle", "abstract"]),
    default="geometric",
    help="Visualization style"
)
@click.option(
    "--width",
    type=int,
    default=1920,
    help="Video width"
)
@click.option(
    "--height",
    type=int,
    default=1080,
    help="Video height"
)
@click.option(
    "--fps",
    type=int,
    default=30,
    help="Frames per second"
)
@click.option(
    "--theme",
    type=click.Choice(["cosmic", "neon", "pastel"]),
    default="cosmic",
    help="Color theme"
)
@click.option(
    "--duration",
    type=float,
    default=0,
    help="Duration in seconds (0 for full audio)"
)
def main(input_file, output, style, width, height, fps, theme, duration):
    """Muviz - Convert audio to visualization video

    INPUT_FILE: Path to audio file (wav, mp3, ogg, etc.)
    """
    # Set up output path
    if output is None:
        input_path = Path(input_file)
        output = str(input_path.with_suffix(".mp4"))

    # Create config
    config = VisualizerConfig(
        width=width,
        height=height,
        fps=fps,
        style=style,
        theme=theme
    )

    click.echo(f"Loading audio: {input_file}")
    click.echo(f"Output: {output}")
    click.echo(f"Style: {style}, Theme: {theme}, Resolution: {width}x{height}@{fps}fps")

    try:
        from muviz.audio.analyzer import AudioAnalyzer
        from muviz.visualizer.geometric import GeometricVisualizer
        from muviz.visualizer.particle import ParticleVisualizer
        from muviz.visualizer.abstract import AbstractVisualizer
        from muviz.renderer.frame_generator import FrameGenerator
        from muviz.renderer.video_writer import VideoWriter

        # Analyze audio
        analyzer = AudioAnalyzer()
        analyzer.load_audio(input_file, duration if duration > 0 else None)

        # Update config with audio sample rate
        config.sample_rate = analyzer.sample_rate

        # Select visualizer
        if style == "geometric":
            visualizer = GeometricVisualizer(config)
        elif style == "particle":
            visualizer = ParticleVisualizer(config)
        else:
            visualizer = AbstractVisualizer(config)

        # Generate frames
        click.echo("Generating visualization frames...")
        frame_generator = FrameGenerator(analyzer, visualizer, config)
        frames = frame_generator.generate_frames()

        # Write video
        click.echo("Writing video file...")
        writer = VideoWriter(config)
        writer.write_video(frames, analyzer.audio, output)

        click.echo(f"Done! Video saved to: {output}")

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
