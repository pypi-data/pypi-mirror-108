from setuptools import find_packages, setup
import pathlib

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name='firstimpression',
    packages=find_packages(),
    version='0.1.0',
    description='First Python library',
    long_description=README,
    long_description_content_type='text/markdown',
    author='FirstImpression',
    author_email='programming@firstimpression.nl',
    license='MIT',
    install_requires=[],
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 2.7'
    ],
)
