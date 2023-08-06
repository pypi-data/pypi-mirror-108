from setuptools import setup

setup(
	name='playlistconverter',
	version='0.0.1',
	description='Convert Apple Music to Spotify',
	author='Andrew King',
	author_email='andrewking1597@gmail.com',
	url='',
	packages=['playlistconverter'],
	install_requires=[
	    "apple-music-python",
	    "certifi",
	    "cffi",
	    "chardet",
	    "cryptography",
	    "idna",
	    "pycparser",
	    "PyJWT",
	    "requests",
	    "six",
	    "spotipy",
	    "urllib3"
	]
) #todo read in from requirements.txt instead of listing explicitly