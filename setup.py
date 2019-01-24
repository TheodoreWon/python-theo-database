import setuptools

setuptools.setup(
    name='theo-database',
    version='1.0.2',
    install_requires=['theo-framework', 'pymongo'],
    url='https://github.com/TheodoreWon/python-theo-database',
    license='MIT',
    author='Theodore Won',
    author_email='taehee.won@gmail.com',
    description='theo-database',
    packages=['theo', 'theo.src.database', 'theo.src.comp'],
    # long_description='GitHub : https://github.com/TheodoreWon/python-theo-database',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    zip_safe=False,
)

'''
NOTE: How to make a package and release the software
0. pip install setuptools, pip install wheel, pip install twine
1. python setup.py bdist_wheel
2. cd dist
3. twine upload xxx.whl
'''
