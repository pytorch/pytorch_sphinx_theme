from setuptools import setup

setup(
    name = 'pytorch_sphinx_theme',
    version = '0.0.1',
    author = 'Shift Lab',
    author_email= 'info@shiftlabny.com',
    url="https://github.com/shiftlab/pytorch_sphinx_theme",
    docs_url="https://github.com/shiftlab/pytorch_sphinx_theme",
    description='PyTorch Sphinx Theme',
    py_modules = ['pytorch_sphinx_theme'],
    packages = ['pytorch_sphinx_theme'],
    include_package_data=True,
    license= 'MIT License',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet",
        "Topic :: Software Development :: Documentation"
    ],
)
