from setuptools import setup, find_packages

setup(
    name='quiron',
    version='1.1.0',
    description='A Python package for Hands Recognition using Mediapipe',
    author='iluzioDev',
    author_email='luischinearangel@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'mediapipe>=0.8.7',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
