from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='YTube',
  version='0.0.7',
  description='Youtube Video Downloader for Python',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  long_description_content_type='text/markdown',
  url='',  
  author='Bestin Lalu',
  author_email='bestinlalu.mec@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='youtube', 
  packages=find_packages(),
  install_requires=['pytube', 'moviepy', 'ffmpeg'] 
)