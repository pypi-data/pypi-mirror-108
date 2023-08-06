from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_des = f.read()

setup(
   name='Easy_AI',
   version='1.0.1.3',
   description='My Project Dont Touch',
   long_description = long_des,
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