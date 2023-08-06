import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CL_Auto_Library", # A custom Library
    version="0.0.9",
    author="sieqqc",
    author_email="sieqqc@gmail.com",
    description="A custom Library",
    long_description="A custom Library",
    long_description_content_type="text/markdown",
    url="http://10.21.37.110/corp_sieq/Partner%20Automation%20Testing%20Trial/_git/Custom_Library",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)