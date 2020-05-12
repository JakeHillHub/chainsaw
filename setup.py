import pathlib
from setuptools import setup
from chainsaw.chainsaw import __VERSION__

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='git-chainsaw',
    version=__VERSION__,
    description='A lightweight wrapper around git subtrees that lets you work with many subtrees at once',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/JakeHillHub/port-linker',
    author='Jake Hill',
    author_email='jakehillgithub@gmail.net',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers'
    ],

    keywords='subtree',
    packages=['chainsaw'],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "chainsaw=chainsaw.chainsaw:main",
        ]
    },
)
