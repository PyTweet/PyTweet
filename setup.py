from setuptools import setup, find_packages
import re

version = ''
with open('twitter/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('version is not set')

readme = ''
with open('README.md') as f:
    readme = f.read()


setup(name='PyTweet',
    authors=['Genofield','TheFarGG'],
    url='https://github.com/TheFarGG/PyTweet/',
    version=version,
    packages=find_packages(),
    license='MIT',
    description='A Python wrapper for the Twitter API using twitter APi version 1.1 and 2!',
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[
        "requests"
    ],
    keywords=[
        "PyTweet",
        "pytweet",
        "twitter",
        "tweet.py",
        "twitter.py"
    ],
    python_requires='>=3.7.0',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
      ]
)