from setuptools import setup
setup(
	name = 'FaceRecog2',
	Packages = [ 'FaceRecog2' ],
	version = '1.0.0',
	description = 'A face recognition PAckage',
	author = 'Suranjan Daw',
	author_email = 'spiderrawn@gmail.com',
	license = 'MIT',
	url = 'https://github.com/SrinjoyMaity/Face' ,
	setup_requires=["numpy","keras","opencv-python"],
	install_requires=["numpy","keras","opencv-python"],
	download_url = 'https://github.com/SrinjoyMaity/Face/archive/refs/tags/v1.0.0.tar.gz',
	keywords = ['face recognition', 'algorithm','machine learning','library'],
	classifiers = [],
	python_requires='>=3',
)
	