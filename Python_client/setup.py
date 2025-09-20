from setuptools import setup, find_packages
import os


# Read the README file for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "BIM Portal Python Client"


setup(
    name="bim-portal-client",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,

    # Dependencies
    install_requires=[
        "httpx==0.27.0",
        "pydantic==2.7.1",
        "requests==2.31.0",
        "PyJWT==2.8.0",
        "python-dotenv==1.0.1",
    ],

    # Python version requirement
    python_requires=">=3.8",

    # Package metadata
    description="BIM Portal API Client - Python Client for BIM Portal API interactions",
    long_description=read_readme(),
    long_description_content_type="text/markdown",

    # Author information
    author="Miguel Vega",
    author_email="miguel.vega@planen-bauen40.de",

    # Project URLs
    url="https://github.com/pb40development/bim-portal",


    # Classifiers
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
    ],

    # Keywords for discoverability
    keywords="bim, api, client, construction, building, information, modeling",

    # Entry points (optional - for CLI tools)
    # entry_points={
    #     'console_scripts': [
    #         'bim-portal=client.cli:main',
    #     ],
    # },
)