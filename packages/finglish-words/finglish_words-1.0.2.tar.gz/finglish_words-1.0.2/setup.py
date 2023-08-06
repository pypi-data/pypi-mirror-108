from setuptools import setup


packages = ['.']





lngds = ''' This is code with king package
it use just for fun persion language chating library


===> from finglishV2 import Finglish


to change persion sentence to english type : 

====> fn = Finglish()


===> fn.make_finglish_sentences(sentence:str)


its will return a finglish strings
 '''


setup(name= "finglish_words",

version = "1.0.2",

description = 'Fun modul for persion language people'
,
long_description = lngds,
author = "Ahmad Dehghani",
author_email = 'ahd76money@gmail.com',
license='MIT',

keywords = ['finlish', 'persion', 'bot', 'telegram', 'chat', 'scrapper', 'images', 'videos'],
packages = packages
,

install_requires = [])
