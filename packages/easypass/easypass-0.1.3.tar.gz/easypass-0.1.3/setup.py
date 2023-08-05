import setuptools

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
	name="easypass",
	version="0.1.3",
	author="Uprj",
	description="Модуль для простой генерации паролей и почтовых ящиков",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/uprj/easypass.py",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3.8",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)