import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

INSTALL_REQUIRES = [
    'numpy',
    'pandas',
]

setuptools.setup(
    name="tactrandom",
    version="0.0.1",
    author="TactLabs",
    author_email="praabindhp@gmail.com",
    description="Simple package for Random Utils, Datasets and so on",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tactlabs/tact-random",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=INSTALL_REQUIRES,
    python_requires='>=3.6',
    zip_safe=False
)