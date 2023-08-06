import setuptools

with open("Odyssey/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="OdysseyDB",  # Replace with your own username
    version="0.0.1",
    author="Yixiao Lan",
    author_email="yixiaolan@foxmail.com",
    description="A lightweight migratable file based key-value database with redis-like api and more features.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Eathoublu/OdysseyDB",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)

