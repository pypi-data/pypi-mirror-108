import pathlib
import setuptools
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text(encoding='UTF-16')

# This call to setup() does all the work
setup(
    name="discord.py-message-components",
    version="1.7.2",
    description="The Original discord.py Libary made by Rapptz with implementation of the Discord-Message-Components by mccoderpy(discord-User `mccuber04#2960`)",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/mccoderpy/discord.py-message-components",
    author="mccoder.py",
    author_email="mccuber04@outlook.de",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    include_package_data=True,
    install_requires=["aiohttp", "chardet", "yarl", "async-timeout", "typing-extensions", "attrs", "multidict", "idna"],
    python_requires=">=3.6"
)
