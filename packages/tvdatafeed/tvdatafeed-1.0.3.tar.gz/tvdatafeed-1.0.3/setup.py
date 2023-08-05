from setuptools import setup
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='tvdatafeed',
    version='1.0.3',
    packages=['tvDatafeed'],
    url='https://github.com/StreamAlpha/tvdatafeed/tree/develop',
    license='MIT License',
    author='@StreamAlpha',
    description='TradingView historical data downloader',
    long_description_content_type="text/markdown",
    long_description=long_description,
    keywords=['tvdatafeed', 'stock markets'],
    install_requires=['pandas', 'selenium',
                      'websocket-client', 'chromedriver-autoinstaller'],
    classifiers=[
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License'
    ]

)
