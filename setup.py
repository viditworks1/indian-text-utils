from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="indian-text-utils",
    version="0.1.0",
    author="Vidit",
    description="Utility functions for processing Indian text data - phone numbers, addresses, names, and more",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YOUR-USERNAME/indian-text-utils",  # Update with your actual GitHub username
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Text Processing",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[],
    extras_require={
        "dev": ["pytest>=6.0.0"],
    },
    entry_points={
        "console_scripts": [
            "indian-phone-clean=indian_text_utils.phone_utils:interactive_test",
        ],
    },
)