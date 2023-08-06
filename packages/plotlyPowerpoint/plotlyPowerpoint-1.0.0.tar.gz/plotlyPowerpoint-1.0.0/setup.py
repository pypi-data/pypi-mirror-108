import setuptools 

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="plotlyPowerpoint",
    version="1.0.0",
    author="Jon Boone",
    author_email="jonboone1@gmail.com",
    description="A library using Plotly and Powerpoint to easily generate slides with plotly charts in them",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6"
)