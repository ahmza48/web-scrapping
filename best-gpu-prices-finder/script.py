from bs4 import BeautifulSoup
import requests
import re

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
for page in range(1,total_pages+1):
    url=f'https://www.newegg.com/p/pl?d={prod}&n=4841&page={page}'
    page=requests.get(url).text
    doc=BeautifulSoup(page,'html.parser')
    div=doc.find(class_='item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell')
    items=div.find_all(class_='item-container')
    for item in items:
        # print(item)
        # parent=item.parent
        print()
        # print('parent: ',parent)
        anchor=item.find('a')
        link=anchor['href']
        print(link)
        # item_info=anchor.find_next_sibling
        print()
        item_info=item.find('a',class_='item-title')
        # print(item_info)
        print(item_info.text)
        price_div=item.find('div',class_='item-action')
        price=price_div.find(class_='price-current')
        print(price.strong.text)
        print()
