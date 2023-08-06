#!/usr/bin/env python3
# from distutils.extension import Extension

# TODO: Fix issue with blender not having python headers.
# from Cython.Build import cythonize
# from Cython.Distutils import build_ext
from setuptools import setup

# extensions = Extension(
#     name="cython_build.lic_internal",
#     sources=["./blendernc/core/lic/lic_internal.pyx"],
# )


# class CustomBuildExtCommand(build_ext):
#     """build_ext command for use when numpy headers are needed."""

#     def run(self):

#         # Import numpy here, only when headers are needed
#         import numpy

#         # Add numpy headers to include_dirs
#         self.include_dirs.append(numpy.get_include())

#         # Call original build_ext command
#         build_ext.run(self)


setup(
    name="blendernc",
    version="0.1.3",
    description="Blender add-on to import netCDF",
    url="https://github.com/blendernc/blendernc",
    author="josuemtzmo",
    author_email="josue.martinezmoreno@anu.edu.au",
    license="MIT License",
    packages=[],
    install_requires=["cython", "numpy"],
    zip_safe=True,
    # cmdclass={"build_ext": CustomBuildExtCommand},
    # TODO: Fix issue with blender not having python headers.
    # ext_modules=cythonize([extensions], build_dir="cython_build"),
)
