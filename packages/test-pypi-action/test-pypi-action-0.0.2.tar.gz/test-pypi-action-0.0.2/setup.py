from setuptools import setup, find_packages


with open("requirements.txt", "r") as req_fp:
    required_packages = req_fp.readlines()

# Use README for long description
with open("README.md", "r") as readme_fp:
    long_description = readme_fp.read()

setup(
    name="test-pypi-action",
    version="0.0.2",
    author="Pablo Lecolinet",
    author_email="pablolec@pm.me",
    description="To be deleted.",
    license="GNU GPLv3",
    keywords="",
    url="https://github.com/PabloLec/test-pypi-action",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests", "docs"]),
    entry_points={},
    install_requires=required_packages,
    package_data={},
    include_package_data=True,
    classifiers=[],
)
