import pathlib

from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='PyDocParser',
    version='2.0',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/stautonico/pydocparser',
    license='MIT',
    author='Steve Tautonico',
    author_email='stautonico@gmail.com',
    description='A python client for the DocParser API',
    long_description=README,
    install_requires=["requests>=2.22.0"],
    keywords=["docparser", "API", "wrapper"],
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)
