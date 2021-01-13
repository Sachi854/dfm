from setuptools import setup, find_packages

with open('READMEen.md', 'r') as f:
    readme = f.read()

with open('LICENSE', 'r') as f:
    license = f.read()

setup(
    name='aem',
    version='0.2',
    description='https://github.com/Sachi854/AndroidEmuMacro',
    long_description=readme,
    author='Sachi854',
    author_email='1701002@sendai-nct.jp',
    url='https://github.com/Sachi854/AndroidEmuMacro',
    license=license,
    install_requires=['numpy', 'opencv-python'],
    packages=find_packages(exclude=('tests')),
    test_suite='tests'
)
