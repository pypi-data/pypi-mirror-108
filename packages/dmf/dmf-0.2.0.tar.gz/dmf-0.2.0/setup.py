import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    required = f.read().splitlines()

setuptools.setup(
    name="dmf", # It should be unique name
    version="0.2.0",
    description="The data matching framework for two dataset",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Phan Quoc Toan",
    author_email="quoctoanpk2511@gmail.com",
    url="https://github.com/quoctoanpk2511/matching-framework",
    project_urls={
        'Homepage': 'https://github.com/quoctoanpk2511/matching-framework',
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["dmf"],
    python_requires='>=3.8',
    install_requires=required,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'git-tagup=git_tagup.__main__:main',
            'gtu=git_tagup.__main__:main',
        ],
    },
)
