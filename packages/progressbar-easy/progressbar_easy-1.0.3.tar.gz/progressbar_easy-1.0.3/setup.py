from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='progressbar_easy',
    version='1.0.3',
    description='A simple progressbar to track progress with built in timer',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Braxton Brown',
    author_email='braxton.brown@outlook.com',
    license='MIT',
    classifiers=classifiers,
    keywords='progressbar, progress bar, progressbar_easy, easy progressbar, easy progress bar',
    packages=find_packages(),
    install_requires=['']
)