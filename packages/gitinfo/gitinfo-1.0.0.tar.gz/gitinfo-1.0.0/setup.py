from setuptools import setup, find_packages

def readme():
    with open("README.md") as f:
        _readme = f.read()
    return _readme


setup(
    name="gitinfo",
    version="1.0.0",
    description="Quickly get information about a Github repository",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Folke Ishii",
    author_email="folke.ishii@gmail.com",
    license="MIT",
    python_requires=">=3.7",
    classifies=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Utilities"
    ],
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "gitinfo = gitinfo.gitinfo:main",
        ]
    },
)
