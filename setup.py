from setuptools import find_packages, setup

setup(
    name='rabbit_wrapper',
    version='0.1',
    url='https://github.com/Satellite-Operations-Services-Optimizer/rabbit-wrapper',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        'pika >= 1.3.2',
        'msgpack>=1.0.7'
    ],
    python_requires=">=3.8"
)
