from setuptools import setup


setup(
    name='groupmaker',
    author='Nicholas Hunt-Walker, Ford Fowler',
    author_email='nhuntwalker@gmail.com',
    extras_require={
        'test': ['pytest', 'pytest-cov'],
        'dev': ['ipython']
    },
    package_dir={'': 'src'},
    py_modules=['creator'],
    entry_points={
        'console_scripts': [
            "groups = creator:main"
        ]
    }
)
