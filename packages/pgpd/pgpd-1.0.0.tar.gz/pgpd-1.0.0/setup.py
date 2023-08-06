import setuptools as setup


def find_packages():
    return ['pgpd'] + ['pgpd.'+p for p in setup.find_packages('pgpd')]


requirements = [
    'pandas>=1.1',
    'pygeos>=0.10',
]

setup.setup(
    name='pgpd',
    version='1.0.0',
    author='0phoff',
    description='PyGEOS ExtensionArray for pandas',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    test_suite='test',
    install_requires=requirements,
)
