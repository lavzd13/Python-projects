import requests
from bs4 import BeautifulSoup

url = "https://www.wikipedia.org"

class	WebScrape:
	def	getIndexHtml(self, url: str):
		#Getting the index.html file from the website
		try:
			response = requests.get(url)
			if response.status_code == 200:
				html_content = response.text
				#Writing the html content of the website to the file
				with open('index.html', 'w') as f:
					f.write(html_content)
				print("Success")
			else:
				print(f"Site reuturned status code: {response.status_code}")
		except requests.exceptions.RequestException as e:
			print(f"Error occured: {e}")
		finally:
			return html_content
	def	extractLinks(self, url: str) -> str:
		#Getting html_content of the website using requests
		html_content = ""
		try:
			response = requests.get(url)
			if response.status_code == 200:
				html_content = response.text
			else:
				print(f"Site reuturned status code: {response.status_code}")
		except requests.exceptions.RequestException as e:
			print(f"Error occured: {e}")
		#Extracting the links from the html_content using BeautifulSoup
		mod = BeautifulSoup(html_content, 'html.parser')
		urls = ""
		for link in mod.find_all('a'):
			urls += link.get('href') + '\n'
		#Writing the links in the file
		with open('links.txt', 'w') as f:
			f.write(urls)

scrape = WebScrape()
scrape.extractLinks(url)