import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mymath_pkg_gravada",
    version="1.0.0",
    author="Gopi Prasad R",
    author_email="gp.ravada@gmail.com",
    description="A small math example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    #package_dir={"": "mymth"},
    packages=setuptools.find_packages(where="mymath"),
    python_requires=">=3.6",
)