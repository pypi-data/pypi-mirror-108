import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tecoradors-elunico",
    version="0.2.0",
    author="Thomas Povinelli",
    author_email="author@example.com",
    description="A small collection of decorators I like to use often",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gist.github.com/elunico/bde1125c1c31fae18f64a6437f2fbe03",
    project_urls={
        # "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "tecoradors"},
    packages=setuptools.find_packages(where="tecoradors"),
    python_requires=">=3.6",
)