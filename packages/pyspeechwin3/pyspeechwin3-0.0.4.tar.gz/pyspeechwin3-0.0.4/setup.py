from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='pyspeechwin3',
  version='0.0.4',
  description='Text To Speech Converter',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Sunami Dasgupta',
  author_email='sunamidasgupta@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Text to Speech, pyttsx3, tts for python, text to speech for python, offline text to speech for python',
  packages=find_packages(),
  install_requires=['pypiwin32','pyttsx3'] 
)
