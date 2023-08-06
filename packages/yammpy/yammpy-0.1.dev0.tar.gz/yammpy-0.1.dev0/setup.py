VERSION='0.1.dev0'

from setuptools import setup, Extension

with open("README.md", "r") as doc:
    long_description = doc.read()
    doc.close()

yammpy = Extension('yammpy', sources=['yammpy/yammpy.c'], include_dirs=['yammpy/include'])

setup(
    name="yammpy",
    version=VERSION,
    author="Ajith Ramachandran",
    author_email="ajithar204@gmail.com",
    description="Yet Another Math Module",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/AjithRamachandran/yamm",
    keywords='Mathematics',
    license='MIT',
    packages=['yammpy'],
    tests_require=['unittest'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    ext_modules=[yammpy],
    python_requires='>=3.7',
)
