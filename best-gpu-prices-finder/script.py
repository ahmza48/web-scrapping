from bs4 import BeautifulSoup
import requests
import re

#this script will scrape title, link and price of product user searches from newegg.com 

#supposed product -> rtx 3080

user_input=input('What product do you want to search for?')
if ' ' in user_input:
    prod = user_input.replace(" ", "+")
else:
    prod = user_input

# # Check if the input contains a space
# if user_input.find(' ') != -1:
#     # Replace spaces with '+'
#     prod = user_input.replace(" ", "+")
# else:
#     # No spaces, use the input as is
#     prod = user_input

url=f'https://www.newegg.com/p/pl?d={prod}&n=4841'
page=requests.get(url).text
doc=BeautifulSoup(page,'html.parser')
list_of_pages=doc.find_all('span',class_='list-tool-pagination-text')[0].strong.text
print(list_of_pages)
pages=list_of_pages.split('/')
total_pages=int(pages[1])
print(total_pages)
# page_text = doc.find(class_="list-tool-pagination-text").strong.text
items_found={}
for page in range(1,total_pages+1):
    url=f'https://www.newegg.com/p/pl?d={prod}&n=4841&page={page}'
    page=requests.get(url).text
    doc=BeautifulSoup(page,'html.parser')
    div=doc.find(class_='item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell')
    items=div.find_all(class_='item-container')
    for item in items:
        anchor=item.find('a')
        link=anchor['href']
        # print(link)
        item_info=item.find('a',class_='item-title')
        item_name=item_info.text
        # print(item_info.text)
        price_div=item.find('div',class_='item-action')
        price_tag=price_div.find(class_='price-current')
        price=price_tag.strong.text
        items_found[item_name]={'price':int(price.replace(',','')),'link':link}

# print(items_found)

# items_found.items() it will create all the tuples that'll have key and value pairs key will be item_name and value will be
# dictionary that has price and link
# then we are passing a function telling how we want to sort it, this is an anonymous function that takes one parameter x which
# will be all of these items, then we say x[1] -> this will give us second item that is dictionary(price + link) and then ['price'] tells sort it by price
# this will return list of tuples

sorted_items=sorted(items_found.items(), key=lambda x: x[1]['price'])
# print(sorted_items)
for item in sorted_items:
    print(item[0])
    print(item[1]['price'])
    print(item[1]['link'])
    print()