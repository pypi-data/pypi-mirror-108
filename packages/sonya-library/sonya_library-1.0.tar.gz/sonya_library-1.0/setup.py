import setuptools
with open(r'D:\Репозиторий\myrepository1\sonya_progect\README.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='sonya_library',
	version='1.0',
	author='Sofia_66',
	author_email='Sonushock@gmail.com',
	description='библиотека по обработке текстов',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/SofiaGalinovskaya/sonya_progect',
	packages=['library_sonya'],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)