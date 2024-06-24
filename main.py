import requests
from bs4 import BeautifulSoup
import re
import json
import time


# # Pular / Bora


def pular():
    start_time = time.time()
    pular_dict=[]
    
    url=['https://catalog.onliner.by/conditioners/gree/gwh09agaxak6dna4']

    
    response=requests.get(url[0])
    soup=BeautifulSoup(response.content,'html.parser')
    atribut_a=soup.find_all('a',class_='offers-description-filter-control offers-description-filter-control_switcher js-facet-configurations-link')
    clear_data=url+[x['href'] for x in atribut_a ]

    
    for data in clear_data:
        re_data=re.search(r"[^/]*$",data).group()
        json_url=f'https://catalog.onliner.by/sdapi/shop.api/products/{re_data}/positions?town=all&has_prime_delivery=1&town_id=17030'
        get_json_data=requests.get(json_url)
        json_html=get_json_data.json()
        pular_dict.append({
            'Model':re_data,
        })
        id_shop=[name_shop for name_shop in json_html['shops']]
        price=[price_shop['position_price'] for price_shop in json_html['positions']['primary']]


        for title,price in zip(id_shop,price):
            pular_dict.append({
            'Shop':json_html['shops'][title]['title'],
            'Price':f"{price['amount']} {price['currency']}"
        })
            
            
    end_time = time.time()
    print(pular_dict)
    print(f"Время выполнения: {end_time - start_time:.2f} секунд")        
        


# # Airy / Lyra
def color_conditioner(lst_url):
    start_time = time.time()
    
    conditioner_data=[]
    lst_name_model=None
    url='https://catalog.onliner.by/conditioners/gree/'
    
    
    for key,value in lst_url.items(): 
        for model in value:
            response=requests.get(url+model)
            soup=BeautifulSoup(response.content,'html.parser')
            atribut_a=soup.find_all('a',class_='offers-description-filter-control offers-description-filter-control_switcher js-facet-configurations-link')
            lst_name_model=value+([x['href'] for x in atribut_a ])
            
            
        for data in lst_name_model:
            re_data=re.search(r'[^/]*$',data).group()
            json_url=f'https://catalog.onliner.by/sdapi/shop.api/products/{re_data}/positions?town_id=17030&limit_total=6&has_delivery=1'
            get_json_data=requests.get(json_url)
            json_html=get_json_data.json()
            conditioner_data.append({
                'Model':re_data,
            })
            id_shop=[name_shop for name_shop in json_html['shops']]
            price=[price_shop['position_price'] for price_shop in json_html['positions']['primary']]
            
            
            for title,price in zip(id_shop,price):
                conditioner_data.append({
                'Shop':json_html['shops'][title]['title'],
                'Price':f"{price['amount']} {price['currency']}"
            })
    

    print(conditioner_data)
    end_time = time.time()
    print(f"Время выполнения: {end_time - start_time:.2f} секунд")   
lst_url={
    'airy':['gwh09avcxbk6dnaw','gwh09avcxbk6dnab','gwh09avcxbk6dnac'],
    'lyra':['gwh09acck6dna1fw','gwh09acck6dna1f','gwh09acck6dna1fh']
    
}
color_conditioner(lst_url)
pular()