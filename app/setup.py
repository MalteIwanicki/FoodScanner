from setuptools import setup, find_packages

setup(
    name="foodscanner",
    version="0.2",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["run-server=app.web.server:start"],
    },
)

