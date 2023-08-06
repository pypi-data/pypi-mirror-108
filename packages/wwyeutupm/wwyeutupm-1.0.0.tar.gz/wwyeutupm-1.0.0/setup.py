from setuptools import setup, find_packages
 
classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]
 
setup(
    name='wwyeutupm',
    version='1.0.0',
    description='A module that writes python',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',  
    author='its_me',
    author_email='rycepie3909@gmail.com',
    license='MIT', 
    classifiers=classifiers,
    keywords='writer', 
    packages=find_packages(),
    install_requires=['']
)