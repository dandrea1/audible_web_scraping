from bs4 import BeautifulSoup 
import requests
from operator import add
from datetime import datetime
import csv 

# Capture HTML webpage 
response = requests.get("https://www.audible.com/adblbestsellers?creativeId=1642b4d1-12f3-4375-98fa-4938afc1cedc&creativeId=00b943e2-39f7-4416-aa6b-3c2695ade879&pageLoadId=N8fTnwldp6A2r4lA&pageLoadId=PVc4MvgGk3Ls1IKy&pageSize=50&searchCategory=18571951011&ref=a_adblbests_c5_pageSize_3&pf_rd_p=e1595489-c152-4314-a5d7-ed60b7e2ecc8&pf_rd_r=AS9WK3CS3BSJ1MXKY0ZZ&pageLoadId=Yy7GxYjgXJhTywJw&creativeId=0bf0e03f-bb55-481b-b4fd-d67375977170")
audible_webpage = (response.text)

soup = BeautifulSoup(audible_webpage, "html.parser")

# Scrape top 50 biography audibooks data 

headings = soup.find_all("h3", class_="bc-heading")
authors = soup.find_all("li", class_="authorLabel")
narrators = soup.find_all("li", class_="narratorLabel")
runtimes = soup.find_all("li", class_="runtimeLabel")
releasedates = soup.find_all("li", class_="releaseDateLabel")
languages = soup.find_all("li", class_="languageLabel")
ratings = soup.find_all("li", class_="ratingsLabel")

# Prepare data columns for CSV file

del headings[0:3]  # Remove menu links which aren't audible book titles. Now first item in list is the audiobook.
title_data = [heading.text.split(".")[1].strip() for heading in headings]

author_data = [author.text.split(":")[1].strip() for author in authors]

narrator_data = [narrator.text.split(":")[1].strip() for narrator in narrators]

# Get total time of audiobook in mins for ease of analysis later. 
runtime_data = [runtime.text.split(":")[1].strip() for runtime in runtimes]
hours_as_mins = [(int(runtime.split('hrs', 1)[0])*60) for runtime in runtime_data]
mins =[runtime.split('and', 1)[1] for runtime in runtime_data]
mins = [int(min.split('mins', 1)[0]) for min in mins]
runtime_in_min_data = list( map(add, hours_as_mins, mins) )

# Convert Release Date to a date (year/month/day)
releasedate_data = [releasedate.text.split(":")[1].strip() for releasedate in releasedates]
releasedate_data = [datetime.strptime(releasedate, '%m-%d-%y').date() for releasedate in releasedate_data]

stars_data = [rating.text.strip()[0] for rating in ratings]

reviews_data = [rating.text.split('stars')[-1].strip() for rating in ratings]
# Some books have future release date and therefore no reviews yet. Leave reviews as a string to be converted to int later by analyst. 
reviews_data = [review.split('ratings')[0].strip() for review in reviews_data]


# Make a list of lists, with each list referencing one row of data. 
# Example [Title, Author, Narator, Runtime, Released Date, Stars (out of 5), # of Reivews]
top_50_list = []

for _ in range(len(title_data)):
    # print(title_data[_])
    top_50_list.append(
        [
            title_data[_], 
            author_data[_], 
            narrator_data[_],
            runtime_in_min_data[_], 
            releasedate_data[_],
            stars_data[_],
            reviews_data[_]
        ])

column_headers = ['Title',
                 'Author',
                 'Narator',
                 'Runtime', 
                 'Released Date', 
                 'Stars (out of 5)',
                  '# of Reivews']

# top_50_list.insert(0,column_headers)

# Save as CVS

with open('top_audiobook_biographies.csv', 'w', newline='') as audibook_csv:
      
    # using csv.writer method from CSV package
    write = csv.writer(audibook_csv)
      
    write.writerow(column_headers)
    write.writerows(top_50_list) 