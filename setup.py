from setuptools import setup
import os

version_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 
                            "freecad", "pd_features", "version.py")
with open(version_path) as fp:
    exec(fp.read())

setup(name='freecad.pd_features',
      version=str(__version__),
      packages=['freecad',
                'freecad.workbench_starterkit'],
      maintainer="Alex Neufled",
      maintainer_email="alex.d.neufeld@gmail.com",
      url="https://github.com/alexneufeld/freecad_pdfeatures",
      description="More PartDesign Modifier features",
      install_requires=[,],
      include_package_data=True)
