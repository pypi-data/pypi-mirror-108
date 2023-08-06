from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Alamo Algorithm Class Implementation'
LONG_DESCRIPTION = 'Python package that allows the user to use the alamo algorithm for interpolation'

# Setting up
setup(
    name="alamoAlg",
    version=VERSION,
    author="Jackson Curry",
    author_email="<jackson.curry6464@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy'],
    keywords=['python', 'Alamo', 'Interpolation'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)