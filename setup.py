from setuptools import setup, find_packages
setup(
    name = "python-tutum",
    version = "0.6.6",
    packages = find_packages(),
    install_requires = ['requests>=2.2.1'],
    provides = ['tutum'],
    author = "Tutum, Inc.",
    author_email = "info@tutum.co",
    description = "Python Library for Tutum",
    license = "Apache v2",
    keywords = "tutum docker",
    url = "http://www.tutum.co/",
)