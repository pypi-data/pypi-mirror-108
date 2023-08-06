from setuptools import setup

long_description = """
A super-fast Python based Autocomplete library that autocomplete incomplete words using various methods
like dictionary lookup, ML based models, etc.

For more information, please check the official documentation at https://imdeepmind.com/python-completes-you/
"""

setup(
    name="pcy",
    version="0.2.0",
    description="PCY (Python Completes You): Autocomplete library for the Python",
    long_description=long_description,
    url="https://imdeepmind.com/python-completes-you/",
    author="Abhishek Chatterjee",
    author_email="abhishek.chatterjee97@protonmail.com",
    license="MIT",
    project_urls={
        "Bug Tracker": "https://imdeepmind.com/python-completes-you/issues",
        "Documentation": "https://imdeepmind.com/python-completes-you/",
        "Source Code": "https://github.com/imdeepmind/python-completes-you/",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["pcy", "pcy.rule_based", "pcy.rule_based.dictionary"],
    install_requires=["py-progress"],
    extras_require={"tests": ["flake8", "black"]},
    include_package_data=True,
)
