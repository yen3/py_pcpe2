from setuptools import setup, find_packages

def read_requirements():
    with open('./requirements.txt', 'r') as f:
        return f.read().split()

    return []

setup(
    name='pypcpe2',
    version='2.2.0',
    author='yen3',
    author_email='yen3rc@gmail.com',
    packages=find_packages(exclude=['examples', 'tests', 'results',
                                    'core', 'core_src', 'temp']),
    install_requires=read_requirements(),
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=['nose'],
    entry_points={
        'console_scripts': ['max_comsubseq.py=pypcpe2.main:main'],
    },
    url='https://github.com/yen3/pypcpe2',
)
