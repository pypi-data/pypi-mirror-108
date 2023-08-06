import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="battlecruiser",
    version="0.0.1",
    author="XMD",
    description="deep learning library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/flarahome/battlecruiser",
    packages=setuptools.find_packages(),
    classifiers=["Programming Language :: Python :: 3"],
    python_requires='>=3.6',
)
