import setuptools
from glob import glob

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gimmick",
    version="0.2",
    author="Pankaj Rawat",
    author_email="pankajr141@gmail.com",
    description="Libraray contains algo to generate images by learning representation from data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pankajr141/gimmick",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        'tensorflow>=2.3.1',
        'matplotlib',
        'scikit-learn==0.24.2'
    ],
)
