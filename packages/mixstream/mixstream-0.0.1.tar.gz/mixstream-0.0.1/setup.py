#!/usr/bin/env python

from setuptools import setup


# readme
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


# setup
setup(
    name="mixstream",
    version="0.0.1",
    description="MixStream is a C-extension to combine SoundTouch & SDL_mixer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="FoFiX team",
    author_email="contact@fofix.org",
    license="GPLv2+",
    url="https://github.com/fofix/python-mixstream",
    project_urls={
        "Bug Tracker": "https://github.com/fofix/python-mixstream/issues",
    },
    packages=["mixstream"],
    package_data={"mixstream": ["*.dll"]},
    zip_safe=False,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Multimedia",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Software Development :: Libraries",
    ],
    keywords="music vorbis sdl soundtouch",
)
