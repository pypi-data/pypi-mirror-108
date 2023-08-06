from setuptools import find_packages, setup

with open("README.md") as file:
    read_me_description = file.read()

with open("requirements.txt") as r:
    requirements = [i.strip() for i in r]

setup(
    name="paiohttpclient",
    version='0.0.1',
    license='MIT License',
    author="Pylakey",
    author_email="pylakey@protonmail.com",
    description="Easy to use python http client based on aiohttp and pydantic.",
    long_description=read_me_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=requirements,
)
