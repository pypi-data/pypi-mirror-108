import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="WordEmbed",
    version="0.2.0",
    author="Onkar Patil",
    author_email="onkar.patil02@gmail.com",
    description="Train and use word embeddings specific to your data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Patil-Onkar/WordEmbed",
    project_urls={
        "Bug Tracker": "https://github.com/Patil-Onkar/WordEmbed/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "tensorflow",
        "tqdm",
        "numpy",
	"pandas",
        "requests",
    ],     
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
