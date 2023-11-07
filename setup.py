from setuptools import find_packages, setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='rabbit_wrapper',
    version='0.1',
    url='https://github.com/Satellite-Operations-Services-Optimizer/rabbit-wrapper',
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    install_requires=[
        "pika >= 1.3.2",
        "msgpack>=1.0.7"
    ],
    python_requires=">=3.10"
)
