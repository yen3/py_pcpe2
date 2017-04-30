from setuptools import setup, find_packages

setup(
    name = 'pypcpe2',
    version = '2.2.0',
    author = 'yen3',
    author_email = 'yen3rc@gmail.com',
    packages = find_packages(exclude=['examples', 'tests', 'results']),
    include_package_data = True,
    test_suite='nose.collector',
    tests_require=['nose'],
    entry_points = {
        'console_scripts': ['max_comsubseq.py=pypcpe2.main:main'],
    },
    url = 'https://github.com/yen3/py_pcpe2',
)
