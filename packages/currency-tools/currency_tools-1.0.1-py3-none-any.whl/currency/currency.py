import requests
from bs4 import BeautifulSoup as bs
class CurrencyPrice:

    def __init__(self,currency_name="bitcoin"):

        self.url = 'https://arzdigital.com/coins/'
        self.currency_name = currency_name

    def get_list_of_avalebel_currecy(self):

        response = requests.get(self.url).text
        soup = bs(response,'html.parser')
        tbcls = "arz-sort-values-box arz-scroll-body"
        currency_list_tabel = soup.find_all('tbody',{"class":tbcls})
        tr_tag  = currency_list_tabel[0].find_all('tr')
        currency_list_tabel = []
        for currency in range(len(tr_tag)-1):
            cr = tr_tag[currency]['data-name']
            currency_list_tabel.append(cr)
        return currency_list_tabel
    def get_price(self):


        URL = self.url+self.currency_name+"/"

        response = requests.get(URL).text

        soup = bs(response,'html.parser')
        tcls = 'arz-coin-page-data__coin-price-box'
        arz_raw = soup.find_all('div',{"class":tcls})
        data = arz_raw[0].text.split('\n')


        currency_change = data[1].split('%')[0]
        currency_price_dollar = data[1].split('%')[1]
        currency_price_toaman = data[2]
        one_dollar_to_toman = data[3].split(':')[1]
        final_output = {
            "currency_change" : currency_change,
            "currency_price_dollar" : currency_price_dollar,
            "currency_price_toaman" : currency_price_toaman,
            "one_dollar_to_toman" : one_dollar_to_toman

                       }

        return final_output
