import pathlib
from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent.resolve()
long_description = open("README.md").read()

# Requirements
install_requires = open("requirements.txt").read().strip().split("\n")
dev_requires = open("dev-requirements.txt").read().strip().split("\n")

# Human-Readable/Reusable Extras
mssql_connector = "pyodbc==4.0.32"

extras = {
    "mssql": [mssql_connector],
}
dangerous_extras = ["mssql"]  # These extras break on certain platforms
extras["all"] = sum(
    [value for key, value in extras.items() if key not in dangerous_extras], []
)

setup(
    name="fidesops",
    description="Automation engine for privacy requests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ethyca/fidesops",
    entry_points={"console_scripts": ["fidesops=fidesops.cli:cli"]},
    python_requires=">=3.7, <4",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    author="Ethyca, Inc.",
    author_email="fidesteam@ethyca.com",
    license="Apache License 2.0",
    install_requires=install_requires,
    dev_requires=dev_requires,
    extras_require=extras,
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries",
    ],
)
