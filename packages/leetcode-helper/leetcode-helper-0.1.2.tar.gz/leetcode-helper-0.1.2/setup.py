import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="leetcode-helper",
    version="0.1.2",
    author="Gongzq",
    author_email="gongzq5@gmail.com",
    description="Some utils for debug leetcode locally",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Gongzq5/leetcode-helper/",
    packages=setuptools.find_packages(),
    install_requires=['prettytable', 'numpy', 'matplotlib', 'numpy', 'networkx'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)