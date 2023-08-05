from distutils.core import setup
from os.path import exists
from setuptools import setup, find_packages

setup(
    name='vn-phone-number',
    version='0.1',
    license='MIT',
    description='This library help developer easier to normalize vietnam number phone '
                'or classify the provider of this number phone',
    # long_description=open('README.md').read() if exists("README.md") else "",
    author='Minh Tran',
    author_email='minhtc.uet@gmail.com',
    url='https://github.com/minhtcuet/vn-phone-number',
    download_url='https://github.com/minhtcuet/vn-phone-number/archive/v_01.tar.gz',
    keywords=['viet name numberphone', 'vietnam number phone convert', 'code chuyen so dien thoai'],
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
    ],
    packages=find_packages(exclude=['build', 'docs', 'templates']),

)