import time
import requests
import threading
from bs4 import BeautifulSoup

extracting = True

def animate():
	global extracting
	n_dots = 0

	print("\nExtracting the data", end="")
	while extracting:
		if n_dots == 3:
			print(end='\b\b\b', flush=True)
			print(end='   ',    flush=True)
			print(end='\b\b\b', flush=True)
			n_dots = 0
		else:
			print(end='.', flush=True)
			n_dots += 1
		time.sleep(0.3)

class	WebScrape:
	def	getIndexHtml(self, url: str):
		#Getting the index.html file from the website
		try:
			response = requests.get(url)
			if response.status_code == 200:
				html_content = response.text
				soup = BeautifulSoup(html_content, "html.parser")
				#Writing the html content of the website to the file
				with open('index.html', 'w') as f:
					f.write(soup.prettify())
				print("\nData extracted. Successfully created index.html file.")
			else:
				print(f"Site reuturned status code: {response.status_code}")
		except requests.exceptions.RequestException as e:
			print(f"Error occured: {e}")

	def	checkLink(self, link: str) -> bool:
		head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
		try:
			response = requests.get(link, headers=head)
			response.raise_for_status()
			return True
		except requests.exceptions.RequestException as e:
			return False

	def	extractLinks(self, url: str) -> str:
		#Getting html_content of the website using requests
		head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
		html_content = ""
		try:
			response = requests.get(url, headers=head)
			if response.status_code == 200:
				html_content = response.text
			else:
				print(f"Site reuturned status code: {response.status_code}")
		except requests.exceptions.RequestException as e:
			print(f"Error occured: {e}")

		#Extracting the links from the html_content using BeautifulSoup
		mod = BeautifulSoup(html_content, 'html.parser')
		if mod:
			valid_links = []
			invalid_links = []
			for link in mod.find_all(['a', 'link'], href=True):
				href = link.get('href')
				#Checking if link starts with http or https
				if href and href.startswith(('http', 'https')):
					#Checking if link is in our lists. If it is that mean that we already checked that link
					# and that is already in valid_links or invalid_links and with this we are improving
	 				# speed of our code to not do the same job twice. Because if we accessed the same link
	  				# just on the different place that will not affect the validity of link.
					if href not in valid_links and href not in invalid_links:
						if self.checkLink(href):
							valid_links.append(href)
						else:
							invalid_links.append(href)

		#Writing the links in the files
		with open('valid_links.txt', 'w') as f:
			for link in valid_links:
				f.write("".join(link) + "\n")
		if invalid_links:
			with open('invalid_links.txt', 'w') as f:
				for link in invalid_links:
					f.write("".join(link) + "\n")
		print("\nData extracted. Successfully created valid_links.txt and invalid_links.txt.")

def main():
	print("\nEnter 1 for index.html file of web page")
	print("Enter 2 for valid and invalid links from web page")
	print("Enter 3 (will execute option 1 and 2)\n")
	while True:
		selection = 0
		try:
			selection = int(input("Enter: "))
			if selection in range(1,4):
				break
			else:
				print("Please enter valid option(1-3).")
		except ValueError:
			print("Please enter a valid integer.")
	url = ""
	while True:
		url = input("Enter a url (http or https needed): ")
		if url.startswith(('http://', 'https://')):
			break
		else:
			print("\nPlease enter url in a valid format http://example.com or htpps://example.com\n")
	global extracting
	scrape = WebScrape()
	anim_thread = threading.Thread(target=animate)
	anim_thread.start()
	if selection == 1:
		scrape.getIndexHtml(url)
		extracting = False
	elif selection == 2:
		scrape.extractLinks(url)
		extracting = False
	elif selection == 3:
		scrape.getIndexHtml(url)
		scrape.extractLinks(url)
		extracting = False
	anim_thread.join()

if __name__ == "__main__":
	main()