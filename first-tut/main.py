# from bs4 import BeautifulSoup
# import requests
# import re

# # with open('index.html','r') as f:
# #     doc=BeautifulSoup(f,'html.parser')

# # # print(doc.prettify())

# # tag=doc.title
# # # print(tag)
# # tag.string='Hello World'
# # # print(tag.string)

# # tags=doc.find_all('p')[0]
# # print(tags.find_all('b'))

# url='https://www.newegg.com/asrock-radeon-rx-6700-xt-rx6700xt-cld-12g/p/N82E16814930056?Item=N82E16814930056&cm_sp=Homepage_dailydeals-_-P0_14-930-056-_-08232023'
# result=requests.get(url)
# # print(result.text)
# doc=BeautifulSoup(result.text,'html.parser')
# # print(doc.prettify())

# prices=doc.find_all(text='$')
# print(prices)
# parent=prices[0].parent
# print(parent)
# print(parent.find('strong').string)

from bs4 import BeautifulSoup
import re

with open('index2.html','r') as f:
    doc=BeautifulSoup(f,'html.parser')
tag=doc.find('option')
print(tag)
# modifying attributes
tag['value']='something new'
tag['selected']='false'
# adding new attribute
tag['color']='red'
print(tag)
# printing all the attributes of that tag
print(tag.attrs)

# searching for multiple tag names at same time
tags=doc.find_all(['p','option','div'])
print(tags)

# searching for tag with specific string
specific_tag=doc.find_all(['option'],string='Undergraduate')
print(specific_tag)

# searching for tag with specific attribute
specific_tagX=doc.find_all(['option'],value='undergraduate')
print(specific_tagX)

# searching on base of class
classItem=doc.find(class_='btn-item')
print(classItem)
print(classItem.string)
# searching multiple items on base of class
classItems=doc.find_all(class_='btn-item')
print(classItems)

# using regular expression for finding some value
price=doc.find_all(string=re.compile('\$.*'))  #this will search for any value containing $ and any value after that any numbers of time 
# print(price)
for p in price:
    print(p.strip())    #this will remove extra spaces from it

# -------------------------------------
# # limit the number of results
# price=doc.find_all(string=re.compile('\$.*'),limit=1)
# # print(price)
# for p in price:
#     print(p.strip())

# modifying the document
inputs=doc.find_all('input',type='text')
for input in inputs:
    input['placeholder']='I changed you'

# saving the changes 
with open('changed.html','w') as file:
    file.write(str(doc))


