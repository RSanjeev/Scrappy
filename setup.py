import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Scrappy",
    version="0.0.1",
    author="",
    author_email="",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RSanjeev/Scrappy.git",
    project_urls={
        "Bug Tracker": "https://github.com/RSanjeev/Scrappy.git",
    },
    classifiers=[
    ],
    install_requires=[
        'requests',
        'beautifulsoup4'
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where=".", exclude=['tests']),
    python_requires=">=3.6",
)
