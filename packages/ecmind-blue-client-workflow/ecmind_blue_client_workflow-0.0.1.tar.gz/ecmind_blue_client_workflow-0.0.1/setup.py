import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='ecmind_blue_client_workflow',
    version='0.0.1',
    author='Roland Koller',
    author_email='info@ecmind.ch',
    description='Helper modules for the `ecmind_blue_client` to ease the work with workflows, models and organisations.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.ecmind.ch/open/ecmind_blue_client_workflow',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
    install_requires=[
        'ecmind_blue_client>=0.3.6',
        'XmlElement>=0.3.0'
    ],
    extras_require = { }
)