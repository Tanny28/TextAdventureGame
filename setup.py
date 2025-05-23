# setup.py
from setuptools import setup, find_packages

setup(
    name="adventure-quest-game",
    version="1.0.0",
    description="Advanced Text-Based Adventure Game for Virtunexa Internship",
    author="Tanmay Shinde",
    author_email="shindetanmay282@gmail.com",
    packages=find_packages(),
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Games/Entertainment :: Role-Playing",
        "Topic :: Education",
    ],
    keywords="adventure game python sqlite education internship",
    entry_points={
        "console_scripts": [
            "adventure-game=adventure_quest:main",
            "adventure-launcher=launcher:main",
        ],
    },
)