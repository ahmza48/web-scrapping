from bs4 import BeautifulSoup
import requests

url='https://coinmarketcap.com/'
result=requests.get(url)
# print(result.text)
doc=BeautifulSoup(result.text,'html.parser')
# print(doc.prettify())
tbody=doc.tbody
# print(tbody.prettify())
# this will give all the tags that are inside tbody 
trs=tbody.contents
print('--------------------------')
# trs[0] is first element inside tbody (1st row of table), so trs[0].next_sibling will print 2nd row of table
# print(trs[0].next_sibling)
# print(trs[1].previous_sibling)  #prev sibling

# print(list(trs[1].next_siblings))  #all the siblings after 2nd row of table

# # this will return entire tbody tag
# print(trs[1].parent)
# # print(trs[1].parent.name) #can also do that to print out the name

# # this will return all the table data || (all three are a little different)
# print('descendants',list(trs[1].descendants)) #it returns the descendant elements as well as nested elements also it writes text of elements as well
# print('contents',list(trs[1].contents)) #it returns direct children to that tag
# print('children',list(trs[1].children)) #just gives you the tags that are inside tr tag similar to contents

all_prices={}
# for tr in trs:
#     print('-----------')
#     for td in tr.contents[2:4]:
#         print(td)
#         print()

for tr in trs[:10]:
    name,prixe = tr.contents[2:4]
    coin_name=name.p.string
    coin_price=prixe.span.string
    # print(coin_name)
    # print(coin_price)
    all_prices[coin_name]=coin_price

print(all_prices)