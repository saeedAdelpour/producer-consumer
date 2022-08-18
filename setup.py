import setuptools

with open("README.md", "r") as fp:
    long_description = fp.read()


setuptools.setup(
    name="producer_consumer",
    version="0.1",
    # scripts=["dokr"],
    author="saeed adelpour",
    author_email="saeed@adelpour99@gmail.com",
    description="An async producer consumer class",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/saeedAdelpour/producer-consumer",
    packages=["producer_consumer"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
