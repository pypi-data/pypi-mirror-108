from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'A Covid model'
LONG_DESCRIPTION = 'This is a simple multiple wave simulation of COVID-19 active cases using sum of Gaussian waves as an approximation'

classifiers=[
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Education",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Operating System :: Microsoft :: Windows"
]

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="multiple_wave", 
    version=VERSION,
    author="Krishna Harsha",
    author_email="<khkrishnaharsha123@gmail.com>",
    url="",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    License="MIT",
    classifiers=classifiers,
    packages=find_packages(),
    install_requires=[], # add any additional packages that         
    keywords=['python', 'covid','multiple waves','second wave','gaussian']
 )
