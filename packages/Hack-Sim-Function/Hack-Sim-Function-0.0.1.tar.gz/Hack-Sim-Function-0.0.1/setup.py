import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Hack-Sim-Function",
    version="0.0.1",
    author="Ömer Rasim",
    author_email="orsmes6145@gmail.com",
    description="Functions for my Game",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kafalar-Karisik/Hack-Simulator/tree/main/Hack-Sim-Functiont",
    project_urls={
        "Bug Tracker": "https://github.com/Kafalar-Karisik/Hack-Simulator/issues",
        "Author Web Site": "https://kafalar-karisik.github.io",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    python_requires=">=3.6",
)
