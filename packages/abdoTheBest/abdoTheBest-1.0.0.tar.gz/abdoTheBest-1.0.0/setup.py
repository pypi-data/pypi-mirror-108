import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="abdoTheBest",
    version="1.0.0",
    author="Fahed Sabellioglu, Abdelrahman Mahmoud",
    author_email="abdohossan@gmail.com, sabellioglu@gmail.com",
    packages=["abdoTheBest"],
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gituser/example-pkg",
    license='MIT',
    python_requires='>=3.0',

)