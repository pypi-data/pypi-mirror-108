import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="NestyDict",
    version="0.0.3",
    author="Kieran Lavelle",
    author_email="kmplavelle@gmail.com",
    description="A package to enable setting and getting of nested dictionaries using paths.",
    long_description=long_description,
    url="https://github.com/kieranlavelle/nestydict",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)