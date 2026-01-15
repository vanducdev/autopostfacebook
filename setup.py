"""
Setup script cho Facebook Auto Post Tool
"""

from setuptools import setup, find_packages
import os

# Đọc file README
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Đọc requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="facebook-auto-post",
    version="1.0.0",
    author="Trần Minh Triết",
    author_email="",
    description="Công cụ tự động đăng bài lên Facebook",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/facebook-auto-post",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "facebook-auto-post=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md", "*.bat"],
    },
)
