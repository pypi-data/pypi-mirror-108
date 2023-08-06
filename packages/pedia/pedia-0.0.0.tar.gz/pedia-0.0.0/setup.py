from setuptools import setup, find_packages

version = '0.0.0'

long_description = ''

setup(
    name="pedia",
    packages=find_packages(exclude=[]),
    version=version,
    description=(
        "Pedia. "
        "Datasets."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="The Pedia Authors",
    author_email="limsweekiat@gmail.com",
    url="",
    license="Apache License 2.0",
    keywords=[
    ],
    install_requires=[
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)