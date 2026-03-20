from setuptools import setup, Extension
import pybind11

ext = Extension(
    'queue_stl',
    sources=['queue_stl.cpp'],
    include_dirs=[pybind11.get_include()],
    language='c++',
    extra_compile_args=['-std=c++11']
)

setup(name='queue_stl', ext_modules=[ext])