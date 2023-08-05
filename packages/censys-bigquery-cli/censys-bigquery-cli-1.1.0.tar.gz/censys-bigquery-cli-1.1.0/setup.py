"""Censys Bigquery Setup."""
import os
from setuptools import setup

GIT_URL = "https://github.com/censys/censys-bigquery"

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = "\n" + f.read()

setup(
    name="censys-bigquery-cli",
    version="1.1.0",
    description="A command line tool for Censys Enterprise Customers that allows BQ access via the command line.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Censys Team",
    author_email="support@censys.io",
    license="Apache License, Version 2.0",
    python_requires=">=3.6.0",
    packages=["censys_bigquery"],
    zip_safe=False,
    install_requires=["google-cloud-bigquery==1.18.0", "google-cloud-core==1.0.3"],
    extras_require={
        "dev": [
            "flake8==3.9.2",
            "flake8-docstrings==1.6.0",
            "flake8-pytest-style==1.4.1",
            "flake8-simplify==0.14.1",
            "flake8-comprehensions==3.5.0",
            "pep8-naming==0.11.1",
            "flake8-black==0.2.1",
            "black==21.5b1",
            "pytest==6.2.4",
            "pytest-cov==2.12.0",
            "mypy==0.812",
            "twine==3.4.1",
        ],
    },
    entry_points={
        "console_scripts": ["censys_bq=censys_bigquery.cli:main"],
    },
    keywords=["censys", "bigquery", "cli"],
    classifiers=[
        "Topic :: Internet",
        "Topic :: Security",
        "Environment :: Console",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    project_urls={
        "Censys Homepage": "https://censys.io/",
        "Changelog": GIT_URL + "/releases",
        "Tracker": GIT_URL + "/issues",
        "Source": GIT_URL,
    },
)
