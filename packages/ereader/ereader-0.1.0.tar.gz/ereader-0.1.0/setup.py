from setuptools import setup
setup(
    name='ereader',
    version='0.1.0',
    author="Himaster",
    author_email="himaster@inbox.ru",
    description="GCP Error Reporting reading tool",
    packages=['ereader'],
    python_requires="==2.7.*",
    install_requires=[
        'cachetools == 3.1.1',
        'certifi == 2021.5.30',
        'chardet == 4.0.0',
        'enum34 == 1.1.10',
        'futures == 3.3.0',
        'google-api-core == 1.29.0',
        'google-auth == 1.30.1',
        'google-cloud-core == 1.6.0',
        'google-cloud-error-reporting == 0.34.0',
        'google-cloud-logging == 1.15.1',
        'googleapis-common-protos == 1.52.0',
        'grpcio == 1.38.0',
        'idna == 2.10',
        'packaging == 20.9',
        'protobuf == 3.17.2',
        'pyasn1 == 0.4.8',
        'pyasn1-modules == 0.2.8',
        'pyparsing == 2.4.7',
        'pytz == 2021.1',
        'requests == 2.25.1',
        'rsa == 4.5',
        'six == 1.16.0',
        'urllib3 == 1.26.5'
    ],
    entry_points={
        'console_scripts': [
            'ereader = ereader.__main__:main'
        ]
    })
