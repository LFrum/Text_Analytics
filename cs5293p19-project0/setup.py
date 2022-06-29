from setuptools import setup, find_packages

setup(
        name='project0',
        version='1.0',
        author='Lince Rumainum',
        author_email='lince.f.rumainum-1@ou.com',
        packages=find_packages(exclude=('tests', 'docs')),
        setup_requires=['pytest-runner'],
        tests_require=['pytest']
)