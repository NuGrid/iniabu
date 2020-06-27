import setuptools

# VARIABLES #

with open("README.rst", "r") as fh:
    long_description = fh.read()

INSTALL_REQUIRES = ["numpy"]

CLASSIFIERS = [
    "Development Status :: 1 - Planning",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    "Intended Audience :: Science/Research",
    "Topic :: Scientific/Engineering",
    "Topic :: Scientific/Engineering :: Physics",
]

# SETUP #

setuptools.setup(
    name="iniabu",  # Replace with your own username
    version="0.9.0",
    author="Reto Trappitsch",
    description="Simple access to initial solar system elemental and isotopic "
    "abundances",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    project_urls={
        "Documentation": "https://iniabu.readthedocs.io",  # todo version
        "Source": "https://github.com/galactic-forensics/iniabu",
    },
    packages=setuptools.find_packages(),
    install_requires=INSTALL_REQUIRES,
    classifiers=CLASSIFIERS,
    python_requires=">=3.5",
)
