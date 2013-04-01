from setuptools import setup, find_packages

version = '0.1'

requires = []

setup(
    name='qbin',
    version=version,
    description="Gentoo Binary Package Manager",
    long_description="qbin is a system for managing Gentoo binary packages.",
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[],
    keywords='',
    author='Ryan Bourgeois',
    author_email='bluedragonx@gmail.com',
    url='https://github.com/BlueDragonX/qbin',
    license='GPLv2',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=requires,
    test_suite="",
    entry_points={
        'console_scripts': [
            'qbin-test-mount=qbin.bin:test_mount',
            'qbin-test-untar=qbin.bin:test_untar',
        ]
    }
)
