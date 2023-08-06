from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Pack command: python setup.py sdist bdist_wheel
# Upload: twine upload dist/*

setup(
    name="toolbox-cli",
    version="0.0.6",
    author="meowmeowcat",
    author_email="",
    description="A toolbox that runs in Command Line Interface.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["toolbox"],
    entry_points='''
        [console_scripts]
        toolbox=toolbox.__main__:cli
    ''',
    python_requires=">=3.6",
    install_requires=[
        "colorama"
    ],
    
)