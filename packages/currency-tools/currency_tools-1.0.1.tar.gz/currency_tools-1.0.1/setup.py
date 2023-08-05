from setuptools import setup


packages = ['currency']





lngds = ''' This is code with king package
you can get currency info online


===> from currency.currency import CurrencyPrice


to get list of avalebel currency use this : 

====> cp = CurrencyPrice(currency_name='bitcoin')
====> cp.get_list_of_avalebel_currecy()


to get a currency info use this :


===> cp.get_price()


its will return a dictionary 
 '''


setup(name= "currency_tools",

version = "1.0.1",

description = 'this method use for who like work with cripto currency'
,
long_description = lngds,
author = "Ahmad Dehghani",
author_email = 'ahd76money@gmail.com',
license='MIT',
url = 'https://github.com/jacktamin/cripto_currency',

  keywords = ['scraping', 'cripto', 'bitcoin', 'currency', 'api', 'scrapper', 'images', 'videos'],
packages = packages
,

install_requires = ['requests','bs4'])
