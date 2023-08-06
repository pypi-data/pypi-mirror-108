"""setup.py: setuptools control."""

from setuptools import setup

version = '0.0.1'

description = "A patch making tool for BDHotfix."

with open('README.md', encoding='utf-8') as fp:
    long_description = fp.read()

install_requires = []
with open('requirements.txt', encoding='utf-8') as fp:
    for line in fp.readlines():
        line = line.strip()
        install_requires.append(line)

setup(
    name="BDHotfixPatchTool",
    version=version,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="zhuyuanqing",
    author_email="zhuyuanqing@bytedance.com",
    url="https://example.com",

    include_package_data=True,
    packages=["BDHotfixPatchTool"],
    entry_points={
        "console_scripts": ['makePatch = BDHotfixPatchTool.patchTool:makePatch']  # BDHotfixPatchTool module - patchTool.py file - makePatch function
    },
    install_requires=install_requires,
    license='MIT',
    platforms=['macOS']
)
