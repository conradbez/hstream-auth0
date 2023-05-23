from setuptools import setup, find_packages

setup(
    name='hstream-auth0',
    version='0.1.0',
    description='A Python package for integrating with Auth0',
    author='Conrad',
    author_email='conradbez1@gmail.com',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
        'python-jose>=3.2.0',
    ],
    python_requires=">=3.6",
    classifiers=[
        'Programming Language :: Python :: 3.10',
    ],
)
