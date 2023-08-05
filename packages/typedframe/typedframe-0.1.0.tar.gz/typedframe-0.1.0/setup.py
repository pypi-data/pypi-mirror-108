import pathlib
import typedframe
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()


setup(
    name="typedframe",
    version=typedframe.__version__,
    description="Typed Wrappers over Pandas DataFrames with schema validation",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/areshytko/typedframe",
    author="Alexander Reshytko",
    author_email="alexander@reshytko.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["typedframe"],
    install_requires=["numpy", "pandas"],
    setup_requires=['pytest-runner'],
    tests_require=['pytest']
)