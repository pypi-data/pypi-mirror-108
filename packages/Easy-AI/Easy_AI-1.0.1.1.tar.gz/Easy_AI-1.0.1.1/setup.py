from setuptools import setup

def readme():
    with open('README.md') as f:
        f.read()

setup(
   name='Easy_AI',
   version='1.0.1.1',
   description='My Project Dont Touch',
   long_description = readme(),
   long_description_content_type='text/markdown',
   author='Khoa1468',
   author_email='khoalam1468@gmail.com',
   packages=['Easy_AI'],  #same as name
   install_requires=[
       'pyttsx3',
       'SpeechRecognition',
       'gtts',
       'playsound'
   ], #external packages as dependencies
)