import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AeroSAM_logger",
    version="0.0.23",
    author="Joseph Girdwood",
    author_email="j.girdwood@herts.ac.uk",
    description="Package for use on a raspberry pi zero, to log MET data from UH-AeroSAM1.3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JGirdwood/AeroSAM_logger",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
)
