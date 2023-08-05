import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="YAPBWD",
    version="0.0.1",
    author="Serg_Sel",
    author_email="seregasel44@gmail.com",
    description="Yet Another Profiler But With Decorators",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SergSel2006/YAPBWD",
    project_urls={
        "Bug Tracker": "https://github.com/SergSel2006/YAPBWD/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
