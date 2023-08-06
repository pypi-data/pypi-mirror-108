from setuptools import setup

with open('readme.md', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='leboncoin',
    url="https://github.com/Shinyhero36/Leboncoin-API-Wrapper",
    description="This is a description",
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.3.5',
    license="GNU General Public License v3.0",
    project_urls={
        'Source': 'https://github.com/Shinyhero36/Leboncoin-API-Wrapper/',
        'Tracker': 'https://github.com/Shinyhero36/Leboncoin-API-Wrapper/issues',
    },
    python_requires='>=3.6',
    install_requires=[
        'requests >= 2.25.0',
        'cloudscraper >= 1.2.48',
    ],
    author="Shinyhero36",
    setup_requires=['setuptools_scm'],  # Automatically include Ressources files
    include_package_data=True,
    packages=['leboncoin'],
)
