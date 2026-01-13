from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nationwide-balance-viewer",
    version="0.1.0",
    author="Mark Retallack",
    description="CLI tool for viewing Nationwide Building Society account balances",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.11",
    install_requires=[
        "selenium>=4.15.0",
        "undetected-chromedriver>=3.5.0",
        "beautifulsoup4>=4.12.0",
        "requests>=2.31.0",
        "click>=8.1.0",
        "cryptography>=41.0.0",
        "keyring>=24.0.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "nationwide-balance=src.cli:main",
        ],
    },
)
