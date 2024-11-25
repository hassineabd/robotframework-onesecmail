from setuptools import setup, find_packages
from os.path import abspath, dirname, join

CURDIR = dirname(abspath(__file__))

CLASSIFIERS = '''
[
Development Status :: 4 - Beta
Intended Audience :: QA Engineers
Programming Language :: Python :: 3.10
Operating System :: OS Independent
Programming Language :: Python :: 3.10
Topic :: Software Development :: Testing
Framework :: Robot Framework
Framework :: Robot Framework :: Library
'''.strip().splitlines()

with open(join(CURDIR, 'readme.md')) as f:
    DESCRIPTION = f.read()
with open(join(CURDIR, 'requirements.txt')) as f:
    REQUIREMENTS = f.read().splitlines()


setup(
    name='OneSecMail',
    version='0.1.0',
    description=DESCRIPTION,
    author='Abdelkader HASSINE',
    author_email='contact.abdelkaderhassine@gmail.com',
    # url='https://github.com/hassineabd/robotframework-onesecmail',
    packages=find_packages(exclude=["docs", "tests", ]),
    include_package_data=True,
    install_requires=REQUIREMENTS,
    # install_requires=[
    #     "robotframework>=4.0.0",
    # ],
    classifiers=CLASSIFIERS,
    python_requires='>=3.10',
)
