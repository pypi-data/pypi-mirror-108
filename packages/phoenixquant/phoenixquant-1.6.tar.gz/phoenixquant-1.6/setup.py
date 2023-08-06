
from setuptools import setup

setup(
    name='phoenixquant',
    version='1.6',
    license='MIT',
    description='This is PhoenixQuant API',
    author='Aaron Qiu',
    author_email='chiminyau@gmail.com',
    url='https://www.phoenixquant.com',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3',
    packages=['phoenixquant'],
    install_requires=[
        "pandas",
        "zmq",
    ]
)