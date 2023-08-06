import pathlib

from setuptools import setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='cowin-app-services',
    version='0.0.3',
    description='Python Library for CoWin API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=' ',
    author='Taranvir Singh Saini',
    author_email='taranvir.554@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Environment :: Console',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='cowin, covid, vaccine',
    packages=['cowin_api'],
    include_package_data=True,
    python_requires='>=3.6, <4',
    install_requires=[
        'fake-useragent==0.1.11',
        'pytest==6.2.3',
        'requests==2.25.1'
    ]
)
