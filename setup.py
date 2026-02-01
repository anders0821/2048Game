from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="2048Game",
    version="1.0.0",
    author="2048 Game Team",
    author_email="dev@2048game.local",
    description="A 2048 puzzle game implemented with PySide6 featuring smooth animations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Topic :: Games/Entertainment :: Puzzle Games",
    ],
    python_requires=">=3.12",
    install_requires=[
        "PySide6>=6.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.950",
        ],
    },
)