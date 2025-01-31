from setuptools import setup, find_packages

setup(
    name="automatic_email",
    version="0.1.0",
    author="DonJuanchox",
    author_email="your_email@example.com",
    description="A module for automating email sending",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/DonJuanchox/OOP",
    packages=find_packages(),
    install_requires=[
        "smtplib",  # Standard library, remove if unnecessary
        "email"  # Standard library, remove if unnecessary
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)