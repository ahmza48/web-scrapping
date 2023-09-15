import csv
from bs4 import BeautifulSoup
import requests

url='https://www.imdb.com/chart/top/'

# to bypass restrictions use following headers
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
listOfMovies=[]

try:
    page=requests.get(url,headers=headers)
    print(page)
    doc=BeautifulSoup(page.text,'html.parser')
    # print(doc.prettify())
    movies_container=doc.find('ul',class_='ipc-metadata-list')
    movies_list=movies_container.find_all('li',class_='ipc-metadata-list-summary-item')
    # print(movies_list)
    for movie in movies_list:
        movieDetails={}
        name_with_rank=movie.find('h3',class_="ipc-title__text").text
        name_with_rank=name_with_rank.split('.')
        rank=name_with_rank[0]
        name=name_with_rank[1].lstrip()
        movieDetails['rank']=rank
        movieDetails['name']=name
        release_year=movie.find('span',class_='sc-b51a3d33-6').text
        movieDetails['release year']=release_year
        detailed_rating=movie.find('span',class_='ipc-rating-star').text
        # detailed_rating contains both the rating and vote count
        detailed_rating=detailed_rating.split('(')
        rating=detailed_rating[0].strip()
        movieDetails['rating']=rating
        listOfMovies.append(movieDetails)
except Exception as e:
    print(e)

# for movie in listOfMovies:
#     print(movie)


# Define the CSV file name and headers
csv_file = 'imdb_movies_data.csv'
csv_headers = ['rank', 'name', 'release year', 'rating']

# Write the data to the CSV file
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=csv_headers)
    writer.writeheader()
    for movie in listOfMovies:
        writer.writerow(movie)

print(f'Data has been saved to {csv_file}')