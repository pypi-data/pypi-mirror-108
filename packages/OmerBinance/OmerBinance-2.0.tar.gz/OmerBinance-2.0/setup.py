import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="OmerBinance",
    version="2.0",
    author="Omer Cerrahpasa",
    author_email="omer.cp61@gmail.com",
    description="TRbinance API implementation in python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["OmerBinance"],
    package_data = {"OmerBinance":["constants.json"]},
    python_requires=">=3.6",
)