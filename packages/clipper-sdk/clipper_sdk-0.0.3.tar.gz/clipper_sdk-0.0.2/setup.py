import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="clipper_sdk",
    version="0.0.2",
    author="ClipperData",
    author_email="support@clipperdata.com",
    description="Python wrapper around the Clipper API client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ClipperData-IT/API_documentation",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    py_modules=["clipper_sdk"],
    install_requires=[
        'colorama',
        'pandas'
        ]
)
