import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pySCILTagger",
    version="0.0.3",
    author="Max Schwartz, Jeremy Macks",
    author_email="schwam4@rpi.edu, macksj@rpi.edu",
    description="A dialog-act tagger for pySCIL.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.rpi.edu/LACAI/pySCIL-Tagger",
    project_urls={
        "Documentation": "https://github.rpi.edu/LACAI/pySCIL-Tagger",
        "Source Code": "https://github.rpi.edu/LACAI/pySCIL-Tagger",
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    zip_safe=False,
)