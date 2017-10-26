from setuptools import setup


setup(
    name='groupmaker',
    author='Nicholas Hunt-Walker, Ford Fowler',
    author_email='nhuntwalker@gmail.com',
    extras_require={
        'test': ['pytest', 'pytest-cov', 'faker'],
        'dev': ['ipython']
    },
    package_dir={'': 'src'},
    py_modules=['creator', 'helpers'],
    entry_points={
        'console_scripts': [
            "groups = creator:main",
            "drop = creator:drop_student"
        ]
    }
)
