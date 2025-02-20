from setuptools import setup, find_packages

setup(
    name="swimming-tracker",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "customtkinter>=5.2.0",
    ],
    entry_points={
        "console_scripts": [
            "swimming-tracker=src.main:main",
        ],
    },
)