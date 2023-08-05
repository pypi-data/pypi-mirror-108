from setuptools import setup
from setuptools import find_packages

long_description = '''
mlviz is a high-level machine learning API, written in Python.
mlviz is a visualization and graphics helpers for common machine learning work.
mlviz is compatible with Python 3.6 and is distributed under the MIT license.
'''

setup(
    name='mlviz',
    version='0.1.2',
    description='mlviz is a visualization and graphics helpers for common machine learning work',
    long_description=long_description,
    author='Benjamin Raibaud',
    author_email='braibaud@gmail.com',
    url='https://github.com/braibaud/mlviz',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Artificial Intelligence'
    ],
    install_requires=[
        'numpy',
        'pandas',
        'pillow',
        'matplotlib',
        'seaborn',
        'statsmodels'],
    python_requires='>=3.6',
    packages=find_packages())