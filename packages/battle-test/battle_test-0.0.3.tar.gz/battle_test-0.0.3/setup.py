from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="battle_test",
    version="0.0.3",
    description="A airtest package for battle test.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["battletest"],
    url="https://github.com/virtualeconomy/pyvsystems",
    author="bingo",
    # author_email="developers@v.systems",
    license="MIT",
    packages=["battle_test"],
    install_requires=["airtest>=1.1.11"],
    # python_requires='>=3.4'
)