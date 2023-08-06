from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intendened Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='getLink',
    version='0.0.1',
    description='A short summary about your package',
    Long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Rakesh Bhol',
    author_email='rkbhol1101@gmail.com',
    license='MIT',
    keywords='',
    packages=find_packages(),
    install_requires=['']
)