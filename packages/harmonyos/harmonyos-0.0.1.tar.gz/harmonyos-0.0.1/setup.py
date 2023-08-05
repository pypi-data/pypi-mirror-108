import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="harmonyos",
    version="0.0.1",
    author="ituser",
    author_email="ituser@126.com",
    description="HarmonyOS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/testpage/harmonyos",
    project_urls={
        "Bug Tracker": "https://gitee.com/testpage/harmonyos/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.5",
)
