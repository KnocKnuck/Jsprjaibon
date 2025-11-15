#!/usr/bin/env python3
"""
Setup script for Euromillions ML Predictor

This setup.py is provided for backward compatibility.
The project primarily uses pyproject.toml for modern Python packaging.

Installation:
    pip install -e .                    # Editable/development install
    pip install -e .[dev]               # With development dependencies
    python setup.py install             # Standard installation (legacy)
"""

from setuptools import find_packages, setup

# Read version from package
def get_version():
    """Extract version from package __init__.py"""
    with open("euromillions_ml/__init__.py", "r") as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip('"').strip("'")
    return "0.1.0"


# Read long description from README if available
def get_long_description():
    """Get long description from README file"""
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "ML-powered Euromillions lottery prediction system"


# Read requirements from requirements.txt
def get_requirements(filename="requirements.txt"):
    """Parse requirements from requirements.txt"""
    requirements = []
    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                # Skip comments, empty lines, and special directives
                if line and not line.startswith("#") and not line.startswith("-"):
                    requirements.append(line)
    except FileNotFoundError:
        pass
    return requirements


# Define development dependencies
dev_requirements = [
    "pytest>=7.4.0,<8.0.0",
    "pytest-cov>=4.1.0,<5.0.0",
    "pytest-asyncio>=0.21.0,<1.0.0",
    "pytest-mock>=3.11.0,<4.0.0",
    "black>=23.7.0,<24.0.0",
    "flake8>=6.1.0,<7.0.0",
    "isort>=5.12.0,<6.0.0",
    "mypy>=1.5.0,<2.0.0",
    "pre-commit>=3.3.0,<4.0.0",
]


setup(
    # Package metadata
    name="euromillions-ml",
    version=get_version(),
    description="ML-powered Euromillions lottery prediction system",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Euromillions ML Team",
    author_email="team@example.com",
    url="https://github.com/yourusername/euromillions-ml",
    project_urls={
        "Documentation": "https://github.com/yourusername/euromillions-ml#readme",
        "Source": "https://github.com/yourusername/euromillions-ml",
        "Tracker": "https://github.com/yourusername/euromillions-ml/issues",
    },

    # License and classifiers
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Operating System :: OS Independent",
    ],

    # Package discovery and content
    packages=find_packages(exclude=["tests", "tests.*", "docs"]),
    include_package_data=True,
    package_data={
        "euromillions_ml": ["py.typed"],
    },

    # Python version requirement
    python_requires=">=3.9",

    # Dependencies
    install_requires=get_requirements("requirements.txt"),
    extras_require={
        "dev": dev_requirements,
    },

    # Entry points for CLI
    entry_points={
        "console_scripts": [
            "euromillions=main:app",
        ],
    },

    # Additional metadata
    keywords="euromillions lottery machine-learning prediction lstm random-forest",
    zip_safe=False,
)
