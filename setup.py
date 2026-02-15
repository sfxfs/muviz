"""Setup configuration for muviz"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="muviz",
    version="0.1.0",
    author="Muviz Team",
    description="Audio visualization video generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "librosa>=0.10.0",
        "numpy>=1.21.0",
        "moviepy>=1.0.3",
        "opencv-python>=4.8.0",
        "pillow>=10.0.0",
        "soundfile>=0.12.0",
    ],
    entry_points={
        "console_scripts": [
            "muviz=muviz.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
