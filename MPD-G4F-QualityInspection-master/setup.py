from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in go4fresh/__init__.py
from go4fresh import __version__ as version

setup(
	name="go4fresh",
	version=version,
	description="Go4Fresh",
	author="Mannlowe Information Services Pvt. Ltd.",
	author_email="shrikant.pawar@mannlowe.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
