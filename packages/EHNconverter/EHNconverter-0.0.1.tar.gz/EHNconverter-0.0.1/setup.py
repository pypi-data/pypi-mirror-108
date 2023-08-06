from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='EHNconverter',
    version='0.0.1',
    description='EHN 410 converter.',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Hanro van der Westhuizen',
    author_email='u18141235@tuks.co.za',
    license='MIT',
    classifiers=classifiers,
    keywords='EHN',
    packages=find_packages(),
    install_requires=['']
)