#python3! -- quotes.py -- Scrapes a Goodreads quote page for quotes and authors, then stores all quotes to 'quotes.txt' file and stores all authors to 'authors.txt' file.
import requests, bs4
from requests_html import HTMLSession
from bs4 import BeautifulSoup

#opens text files to write to
quote_file = open("quotes.txt", "w") 
author_file = open("authors.txt", "w")

#Uses requests-html to get our page, then scrapes the page for quotes and authors, storing the information to their relevant text files
def scrape(url):
	session = HTMLSession()
	print(url)
	r = session.get(url)
	r.html.render()
	soup = bs4.BeautifulSoup(r.text, features="lxml")
	text_list = soup.find_all("div", class_= "quoteText")
	for text in text_list:
		text = text.text
		quote = text.split("―",1)[0]
		print(quote)
		quote_file.write(quote)
	author_list = soup.find_all("span", class_= "authorOrTitle")
	for author_text in author_list:
		author_text = author_text.text
		author = author_text.split(",",1)[0]
		print(author)
		author_file.write(author)
	session.close()

#Goes to next page and gets new url.
def get_new_url(i):
	url_end = str(i)
	url = 'https://www.goodreads.com/quotes/tag/business?page=' + url_end
	print('Scraping post links for: ' + url)	
	return url

i = 1
#Will scrape 25 pages.
while i < 26:

	try:

		#Calls the function 'get_new_url' and sets this 'url' variable to its return, which is the url of the next page of quotes and authors to scrape.
		url = get_new_url(i)
			
		#Scrapes for quotes and authors and writes to text files.	
		scrape(url)

		i = i + 1

	#Ends the loop when a url is invalid.	
	except requests.exceptions.RequestException:
		break		

print('Scrape complete.')
quote_file.close()
author_file.close()