from setuptools import setup, Extension
import numpy

with open("README.md", "r") as fh:
    long_description = fh.read()
    fh.close()

seso = Extension('seso', sources=['seso/seso.c'], include_dirs=[numpy.get_include(), 'seso/include'])

setup(
    name="seso",
    version="0.2",
    author="Ajith Ramachandran",
    author_email="ajithar204@gmail.com",
    description="Search and Sort Algorithms",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/AjithRamachandran/seso",
    keywords='search and sort',
    license='MIT',
    packages=['seso'],
    install_requires=['numpy'],
    tests_require=['unittest'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    ext_modules=[seso],
)
