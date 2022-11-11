from setuptools import setup

import py_clc

with open('README.md', encoding='UTF-8') as f:
    long_description = f.read()

setup(
    name='PyCLC',
    version=py_clc.__version__,
    packages=['py_clc'],
    python_requires='>=3.11',
    url='https://github.com/aixcyi/PyCLC',
    license='MIT',
    author='aixcyi',
    author_email='75880483+aixcyi@users.noreply.github.com',
    description='A Python package about Chinese Lunisolar Calendar.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Natural Language :: Chinese (Simplified)",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
        # "Typing :: Typed",
    ],
    keywords=[
        "date", "calendar", "lunisolar", "datetime", "chinese", "time"
    ],
    project_urls={
        "Source": "https://github.com/aixcyi/PyCLC",
        "Tracker": "https://github.com/aixcyi/PyCLC/issues",
    }
)
