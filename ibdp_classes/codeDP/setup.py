from setuptools import setup, find_packages

setup(
    name="codeDP",
    version="0.1",
    packages=find_packages(),
    install_requires=["PyQt5", "ibdp-classes", "sip"],
    entry_points={"console_scripts": ["mypackage=mypackage.main_window:main"]},
)
