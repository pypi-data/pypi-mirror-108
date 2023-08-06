import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hwsis",
    version="0.0.1", # Latest version .
    author="Huawei",
    author_email="huawei@gmail.com",
    description="Huawei SIS.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/huawei/",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
