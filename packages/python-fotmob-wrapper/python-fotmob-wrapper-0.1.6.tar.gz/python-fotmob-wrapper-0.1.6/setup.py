from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup (
        name='python-fotmob-wrapper',
        packages=find_packages(include=['fotmob']),
        version='0.1.6',
        description='Python wrapper for Fotmob',
        author='Andrew Reifman-Packett',
        author_email="reifmanpackett@gmail.com",
        url="https://github.com/AndyReifman/fotmob",
        project_urls={
            "Bug Tracker": "https://github.com/AndyReifman/fotmob/issues",
        },
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        install_requires=[],
        setup_requires=['pytest-runner'],
        tests_require=['pytest==4.4.1'],
        test_suite='test',
        )
