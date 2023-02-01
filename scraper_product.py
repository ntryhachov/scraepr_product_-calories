import requests
from bs4 import BeautifulSoup
import lxml
import random
import time
import csv
from fake_useragent import UserAgent


def product_href(url):
    user = UserAgent()
    headers = {
        'user-agent': user.random
    }
    responce = requests.get(url=url, headers=headers).text
    soup = BeautifulSoup(responce, 'lxml')
    src = soup.find_all("ul")[1:5]
    list_href = []
    for items in src:
        for item in items.find_all("li"):
            list_href.append(f"https://calorizator.ru/{item.find('a').get('href')}")
    return list_href

def prod_parans(url):
    user = UserAgent()
    headers = {
        'user-agent': user.random
    }
    responce = requests.get(url=url, headers=headers).text
    soup = BeautifulSoup(responce, 'lxml')
    product_name = soup.find(class_="views-field views-field-title active").text
    protein = soup.find(class_="views-field views-field-field-protein-value").text
    fat = soup.find(class_="views-field views-field-field-fat-value").text
    carbohydrate = soup.find(class_="views-field views-field-field-carbohydrate-value").text
    kcal = soup.find(class_="views-field views-field-field-kcal-value").text
    time.sleep(random.randint(2, 5))
    with open ('products.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow([product_name, protein, fat, carbohydrate, kcal])
def product_result(list_href):
    for href in list_href:
        user = UserAgent()
        headers = {
            'user-aget': user.random
        }
        responce = requests.get(url=href, headers=headers).text
        soup = BeautifulSoup(responce, 'lxml')
        if soup.find('ul', class_="pager") is not None:
            user = UserAgent()
            url = f"{href}?page"
            headers = {
                'user-agent': user.random
            }
            responce = requests.get(url=url, headers=headers).text
            soup = BeautifulSoup(responce, 'lxml')
            search = soup.find('ul', class_="pager").text.replace("\n", "")[-1]
            for page in range(int(search)):
                src = soup.find_all('tr', {'class': {"odd views-row-first", "odd", "even"}})
                src = [i.text.strip().replace("\n", ",") for i in src]
                time.sleep(random.randint(2,5))
                for item in src:
                    b = item.split(",")
                    b = [i for i in b if i != ""]
                    with open('products.csv', 'a') as file:
                        writer = csv.writer(file)
                        writer.writerow(b)
        else:
            src = soup.find_all('tr', {'class': {"odd views-row-first", "odd", "even"}})
            src = [i.text.strip().replace("\n", ",") for i in src]
            for i in src:
                b = i.split(",")
                b = [i for i in b if i != ""]
                with open('products.csv', 'a') as file:
                    writer = csv.writer(file)
                    writer.writerow(b)


#
#
#
#
def main():
    url = "https://calorizator.ru/product"
    list_href = product_href(url)
    prod_parans(list_href[0])
    product_result(list_href)
#
#
if __name__ == "__main__":
    main()
