import setuptools
from codecs import open
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="objectlink-core",
    version="v0.2",
    description="ObjectLink protocol support for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/apigear-io/objectlink-core-python",
    author="ApiGear.io",
    author_email="info@apigear.io",
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Code Generators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='rpc objects apigear',
    extras_require={
        'dev': [
            'websockets',
            'starlette',
        ],
        'test': [
            'pytest',
        ],
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",    
)