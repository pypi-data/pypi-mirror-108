from setuptools import setup

# show readme
with open("README.md", "r") as readme:
    long_description = readme.read()

# setup stuff
setup(
    name='grab-reddit',
    url='https://gitlab.com/RealStickman/grab/',
    author="RealStickman",
    author_email="mrcfrm01@protonmail.com",
    version='0.0.8',
    description='A Reddit download bot',
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["newgrab", "newgrabmod"],
    package_dir={'': 'src'},
    classifiers=[
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 3 - Alpha",
    ],
    install_requires = [
        "praw >= 7.1.0",
    ],
    extras_require = {
        "dev": [

        ],
    },
    entry_points={
        'console_scripts': [
            'grab-download = newgrab:main',
        ]
    },
)
