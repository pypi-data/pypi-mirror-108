import setuptools
import distutils.sysconfig
from setuptools.dist import Distribution

tracker = "optitrack"
setuptools.setup(
   name = tracker,
   version = "0.0.1",
   author = "Ana Soto",
   author_email = "ana.sotodelacruz@gmail.com",
   description = tracker + " c ++ wrapper for python 3.7",
   packages = setuptools.find_packages(),
   package_data={tracker : [tracker+'/*.dll', tracker+'/*.pyd']},
   include_package_data=True,
   classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
   ],
)
