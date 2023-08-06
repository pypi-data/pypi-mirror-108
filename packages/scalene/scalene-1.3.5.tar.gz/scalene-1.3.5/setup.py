from setuptools import setup, find_packages
from distutils.core import Extension
import subprocess
import sys
from scalene.scalene_version import scalene_version

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

try:
    if sys.platform == 'win32':
      cmd = "nmake"
    else:
      cmd = "make"
    out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
except Exception as e:
    if isinstance(e, subprocess.CalledProcessError):
        print("`make` returned non-zero error code:", e.returncode, e.output)
    else:
        print("Unexpected error:", e)
    exit(1)

import sys

if sys.platform == 'win32':
    extra_args = '/std:c++14' # for Visual Studio C++
else:
    extra_args = '-std=c++14' # Clang or g++
    
mmap_hl_spinlock = Extension('get_line_atomic',
                include_dirs=['.', 'vendor/Heap-Layers', 'vendor/Heap-Layers/utility'],
                sources=['src/source/get_line_atomic.cpp'],
                extra_compile_args=[extra_args],
                language="c++14")

setup(
    name="scalene",
    version=scalene_version,
    description="Scalene: A high-resolution, low-overhead CPU, GPU, and memory profiler for Python",
    keywords="performance memory profiler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/emeryberger/scalene",
    author="Emery Berger",
    author_email="emery@cs.umass.edu",
    license="Apache License 2.0",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: IPython",
        "Framework :: Jupyter",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development",
        "Topic :: Software Development :: Debuggers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows :: Windows 10"
    ],
    packages=find_packages(),
    install_requires=[
        "rich>=9.2.10",
        "cloudpickle>=1.5.0",
        "nvidia-ml-py==11.450.51",
        "numpy"
    ],
    ext_modules=[mmap_hl_spinlock],
    setup_requires=['setuptools_scm'],
    include_package_data=True,
    entry_points={"console_scripts": ["scalene = scalene.__main__:main"]},
    python_requires=">=3.7",
)
