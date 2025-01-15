from setuptools import find_packages, setup

setup(
    name="latinuzconverter",
    version="1.0.0",
    description="A simple package to convert latin text to cyrillic and vice versa.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="DavronbekDev",
    author_email="xackercoder@gmail.com",
    url="https://github.com/firdavsdev//UzLatinConverterPyPI",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    # Paket uchun talab qilinadigan kutubxonalarni ko'rsating
    # install_requires=[
    #     "aiohttp>=3.8.0",
    # ],
)
