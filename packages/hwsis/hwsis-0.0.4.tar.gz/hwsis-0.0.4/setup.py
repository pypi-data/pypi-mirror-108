import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hwsis",
    version="0.0.4", # Latest version .
    author="John John",
    author_email="abcdefghigk@gmail.com",
    description="SUCCESS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.google.com/google",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
