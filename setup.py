from setuptools import setup
import re

version = ""
with open("pytweet/__init__.py") as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError("version is not set")

readme = ""
with open("README.md") as f:
    readme = f.read()

requirements = []
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

extras_require = {
    "docs": [
        "sphinx>=4.0.2",
        "furo==2021.11.23",
        "sphinx_copybutton>=0.4.0",
    ],
    "events": ["Flask>=2.0.2"],
}

classifiers = [
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Operating System :: OS Independent",
    "Topic :: Internet",
    "Topic :: Utilities",
    "Development Status :: 5 - Production/Stable",
]

# fmt: off

# fmt: on

setup(
    name="PyTweet",
    author="TheGenocide & TheFarGG",
    maintainer=", ".join(("TheFarGG", "TheGenocide")),
    url="https://github.com/PyTweet/PyTweet/",
    version=version,
    packages=["pytweet", "pytweet.dataclass", "pytweet.threads"],
    include_package_data=True,
    license="MIT",
    project_urls={
        "Documentation": "https://py-tweet.readthedocs.io/",
        "HomePage/Github": "https://github.com/PyTweet/PyTweet/",
        "Discord": "https://discord.gg/XHBhg6A4jJ",
        "Issue tracker": "https://github.com/PyTweet/PyTweet/issues"
    },
    description="A Synchronous python API wrapper for twitter's api",
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    extras_require=extras_require,
    keywords=["PyTweet", "pytweet", "twitter", "tweet.py", "twitter.py"],
    python_requires=">=3.7.0",
    classifiers=classifiers,
)
