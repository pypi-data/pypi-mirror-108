import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yehonatan",
    version="0.0.2",
    author="Yehonatan Harmatz",
    author_email="yehonatan.y@gmail.com",
    description="my python package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yehonatanHarmatz/yehonatan",
    project_urls={
        "Bug Tracker": "https://github.com/yehonatanHarmatz/yehonatan/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
