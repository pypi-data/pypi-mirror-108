from setuptools import setup

with open('readme.md', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='leboncoin',
    url="https://github.com/Shinyhero36/Leboncoin-API-Wrapper",
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.2',
    license='MIT',
    install_requires=[
        'requests >= 2.25.0',
        'cloudscraper >= 1.2.48',
    ],
    author="Shinyhero36",
    setup_requires=['setuptools_scm'],  # Automatically include Ressources files
    include_package_data=True,
    packages=['leboncoin_api_wrapper'],
)
