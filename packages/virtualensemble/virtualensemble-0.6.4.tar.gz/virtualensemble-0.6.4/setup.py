import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This calls to setup() does all the work
setup(
	name="virtualensemble",
	version="0.6.4",
	description="Easily create a mosaic virtual music piece",
	long_description=README,
	long_description_content_type="text/markdown",
	url="",
	author="James Maggs",
	author_email="EmailVirtualEnsemble@gmail.com",
	license="GNU General Public License v3.0",
	classifiers=[
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Natural Language :: English',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3',
	],
	packages=find_packages(),
	include_package_data=True,
	install_requires=["PySide6", "scipy", "numpy", "soundfile", "psutil"],
	entry_points={
		"console_scripts": [
			"virtualensemble=virtualensemble.virtualensemble:main",
		]
	},
)
