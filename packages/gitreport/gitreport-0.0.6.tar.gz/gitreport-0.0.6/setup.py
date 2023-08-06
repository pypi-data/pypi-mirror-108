import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open('requirements.txt') as f:
    requirements = f.readlines()

setuptools.setup(
    name="gitreport",
    version="0.0.6",
    author="monopeelz",
    author_email="monopeelz@gmail.com",
    description="Productivity git report to avoid stupid job in every month",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/peelz/git-report",
    project_urls={
        "Bug Tracker": "https://github.com/peelz/git-report/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'gitreport = src.cli:main'
        ]
    },
    packages=setuptools.find_packages(),
    install_requires=requirements,
    python_requires=">=3.6",
    zip_safe=False
)
