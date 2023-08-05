from setuptools import setup

import apiratelimit

def readme():
    '''Read README file'''
    with open('README.rst') as infile:
        return infile.read()

setup(
    name='apiratelimit',
    version=apiratelimit.__version__,
    description='API rate limit decorator',
    long_description=readme().strip(),
    author='Tomas Basham',
    author_email='me@tomasbasham.co.uk',
    url='https://github.com/chiragkanhasoft/apiratelimit',
    license='MIT',
    packages=['apiratelimit'],
    install_requires=[],
    keywords=[
        'ratelimit',
        'api',
        'decorator'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Topic :: Software Development'
    ],
    include_package_data=True,
    zip_safe=False
)
