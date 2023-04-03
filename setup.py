from setuptools import setup, find_packages

setup(
    name="GPT-linear-regressor",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scikit-learn'
    ],
    python_requires='>=3.9',
    author="Accelerate Science",
    author_email="accelerate-mle@cst.cam.ac.uk",
    description="A linear regression application packaged by GPT-4",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
