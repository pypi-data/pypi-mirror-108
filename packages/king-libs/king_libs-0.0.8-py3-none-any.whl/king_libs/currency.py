import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import os
import matplotlib.pyplot as plt
from dateutil.parser import parse
class  Get_currency_data:

    def __init__(self):
        pass




    @staticmethod
    def get_data(currency_name,max_pages):
        main_data = []
        for page in range(max_pages):
            url = f'https://arzdigital.com/coins/{currency_name}/historical-data/page-{page}/'
            res  = requests.get(url)
            soup  = bs(res.text,'html.parser')
            table = soup.find('table' ,attrs = {'arz-table arz-historical-data-table'})
            tbody = table.find('tbody').find_all('tr')

            for n in range(len(tbody)-1):
                thd = []
                for td in tbody[n].find_all('td')[2:]:
                    thd.append(td.text)

                main_data.append(thd)
        return main_data
    @staticmethod
    def save_dataset(main_data,save_path):

        def delete_dls(target):

            rep = target.replace("$","")
            rep = rep.replace(",","")
            return rep

        def pre_date(date):

            dt = parse(thd[2])

            date = dt.strftime('%d/%m/%Y')

            return date

        prices = []
        shamsi_dates = []
        dates = []
        for dt in range(len(main_data)-1):



            price = delete_dls(main_data[dt][0])[:-2]
            shamsi_date = main_data[dt][1]
            date = main_data[dt][2]
            prices.append(price)
            shamsi_dates.append(shamsi_date)
            dates.append(date)
        data = {f"{save_path}_price":prices,
               'shamsi_date':shamsi_dates,
               'date':dates}
        df = pd.DataFrame(data,index=range(len(prices)))
        df['date'] = pd.to_datetime(df['date']).dt.date
        # root = os.getcwd()
        # os.chdir(root)
        df.to_csv(f'{save_path}.csv',index=False)





