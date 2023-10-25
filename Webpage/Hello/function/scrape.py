import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm
import os
from time import sleep


def scrape(search_query):
    output_directory = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')
    os.makedirs(output_directory, exist_ok=True)
    
    output_file_path = os.path.join(output_directory, f'{search_query}.json')
    
    # Check if the JSON file already exists
    if os.path.exists(output_file_path):
        with open(output_file_path, 'r') as json_file:
            items = json.load(json_file)
        return items
    else:
        items = []
        page = 1
        payload = {'api_key': 'b15b951c8bc84db3cb06223bf644948d', 'url': 'https://www.amazon.in/s?k={0}&page={0}&ref=sr_pg_{0}'.format(search_query, page, page)}

        for i in tqdm(range(1), desc='webpage progress'):
            response = requests.get('http://api.scraperapi.com', params=payload)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            results = soup.find_all('div', {'class': 's-result-item', 'data-component-type': 's-search-result'})

            for result in tqdm(results, desc=f'items in page {i}'):
                product_name = result.h2.text
            
                try :
                    rating = result.find('i', {'class': 'a-icon'}).text
                    rating_count = result.find('span', {'class': 'a-size-base'}).text
                    price = result.find('span', {'class': 'a-price-whole'}).text
                    product_image = result.find("img", class_="s-image")["src"]
                    product_url ='https://amazon.in' + result.a['href']
                    
                    name = product_name.split("|")[0]
                    
                    items.append({
                        'product': name,
                        'rating': rating,
                        'rating_count': rating_count,
                        'price': price,
                        'product_url': product_url,
                        'product_image': product_image
                    })
                except AttributeError:
                    continue

            page += 1
            sleep(1.5)

        with open(output_file_path, 'w') as json_file:
            json.dump(items, json_file, indent=4)

        return items
