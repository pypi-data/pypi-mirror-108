from setuptools import setup, find_packages

versiontext = open('VERSION').read().strip()
licensetext = open('LICENSE').read().strip()

setup(
    name = 'xkye',
    version = versiontext,
    license = licensetext,
    author = 'Rahman Ansari',
    author_email = 'iamrahmanansari@gmail.com',
    url = 'https://github.com/RahmanAnsari/',
    description = 'Official Python Standard Library for Xkye Language',
    long_description = open('PYPIREADME.md').read().strip(),
    long_description_content_type='text/markdown',
    packages = find_packages(),
    install_requires=[
        # put packages here
        'antlr4-python3-runtime',
        'multipledispatch',
    ],
    classifiers= [
        "Development Status :: 5 - Production/Stable",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules"
        ]
)
