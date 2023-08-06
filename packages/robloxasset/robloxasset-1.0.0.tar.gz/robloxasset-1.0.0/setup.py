import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="robloxasset",
    author="hxnter",
    version="1.0.0",
    description="An Wrapper for Roblox Web Asset Api.",
    url="https://github.com/hxnter69/robloxasset",
    download_url="https://github.com/hxnter69/robloxasset/archive/refs/heads/main.zip",
    packages=setuptools.find_packages(),
    classifiers=[],
    install_requires="requests"
)
