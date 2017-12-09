from distutils.core import setup

setup(
    name = 'kcem',
    packages = ['kcem'],
    package_data={'kcem':['utils/*', 'wiki/*', 'wiki/crawler/*']},
    version = '3.1',
    description = 'kcem class file',
    author = 'davidtnfsh',
    author_email = 'davidtnfsh@gmail.com',
    url = 'https://github.com/udicatnchu/kcem',
    download_url = 'https://github.com/udicatnchu/kcem/archive/v3.1.tar.gz',
    keywords = ['kcem'],
    classifiers = [],
    license='GPL3.0',
    install_requires=[
        'pymongo',
        'simplejson',
        'requests',
        'kcmApp',
    ],
    zip_safe=True
)
