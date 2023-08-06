import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

project_name = "idle"
project_version= "1.0.3"
project_author = "Devesh Sharma"
project_description = "Alternavtive of notepad"


setuptools.setup(
    name=project_name,
    version=project_version,
    author=project_author,
    description=project_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["idle"],
    package_dir={'':'idle/src'},
    install_requires=[""]
)
