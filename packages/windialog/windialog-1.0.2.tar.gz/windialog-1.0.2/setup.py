from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

with open('LICENSE.txt') as l:
    L = l.read()

classifiers = [ 'Environment :: Win32 (MS Windows)',
	            'Intended Audience :: Developers',
	            'License :: OSI Approved :: MIT License',
	            'Operating System :: Microsoft :: Windows',
	            'Operating System :: Microsoft :: Windows :: Windows Vista',
	            'Operating System :: Microsoft :: Windows :: Windows 7',
	            'Operating System :: Microsoft :: Windows :: Windows 8',
	            'Operating System :: Microsoft :: Windows :: Windows 8.1',
	            'Operating System :: Microsoft :: Windows :: Windows 10',
	            'Programming Language :: Python :: 3 :: Only',
	            'Programming Language :: Python :: 3.8',
	            'Programming Language :: Python :: 3.9',
	            'Programming Language :: Python :: 3.10',
	          ]

setup_args = dict(
    name='windialog',
    version='1.0.2',
    description='An API to use the new Windows file & folder Dialogue Explorer',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY + '\n\n' + L,
    license='MIT',
    packages=find_packages(),
    classifiers = classifiers,
    author='MissingNo42',
    keywords=['Windows', 'Files', 'Folders', 'Explorer', 'Python 3', 'Python 3.8'],
    url='https://github.com/MissingNo42/windialog',
    download_url='https://pypi.org/project/windialog/'
)

install_requires = []

if __name__ == '__main__':
    setup(**setup_args)
