from setuptools import setup

with open("README.md","r") as fh:
    long_description = fh.read()
setup(
    name='helloworld_by_ariel',
    version='0.0.1',
    description='Say Hello',
    py_modules = ["helloworld"],
    package_dir = {'':'src'},
    long_description = long_description,
    long_description_content_type="text/markdown",
    extras_require={
        "dev":[
            "pytest>=3.7",
        ],
    }
    
)
