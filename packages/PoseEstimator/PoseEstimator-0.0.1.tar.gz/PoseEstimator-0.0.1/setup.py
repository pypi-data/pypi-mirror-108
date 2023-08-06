  
from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Basic Pose estimation Module'
LONG_DESCRIPTION = 'Exploring pose estimation'

# Setting up
setup(
    name="PoseEstimator",
    version=VERSION,
    author="Syed Abdul Gaffar Shakhadri",
    author_email="<syed.17.beec@acharya.ac.in>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['opencv-python', 'mediapipe'],
    keywords=['python', 'pose', 'pose-estimation', 'Pose Estimation', 'opencv pose estimation', 'estimation'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
