import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="GummyFNAsync",
    version="1.0.0",
    author="Pirxcy",
    description="Async Api wrapper for GummyFN",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://api.gummyfn.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'aiohttp',
          'fortnitepy',
      ],
)
