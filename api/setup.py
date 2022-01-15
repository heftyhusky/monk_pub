from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="api",  # Required
    version="1.0.1",  # Required
    description="",  # Optional
    long_description=long_description,  # Optional
    long_description_content_type="",  # Optional (see note above)
    url="",  # Optional
    author="",  # Optional
    author_email="",  # Optional
    classifiers=[  # Optional
    ],
    keywords="",  # Optional
    # packages=find_packages(exclude=["importlib", "pymysql", "pandas"]),
    project_urls={  # Optional

    },
)
