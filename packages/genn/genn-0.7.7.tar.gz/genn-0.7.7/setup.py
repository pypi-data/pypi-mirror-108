import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="genn",
    version="0.7.7",
    author="Fahed Sabellioglu, Abdelrahman Mahmoud",
    author_email="abdohossan@gmail.com, sabellioglu@gmail.com",
    packages=["genn"],
    description="GeNN (Generative Neural Networks) is a high-level interface for text applications using PyTorch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FahedSabellioglu/genn",
    license='MIT',
    python_requires='>=3.0',
    install_requires=[
         "torch",
         "torchtext",
         "pytorch_transformers",
         "fasttext"
    ]
)