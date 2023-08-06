import re
import requests
from bs4 import BeautifulSoup

class Crawler:
	def __init__(self, url):
		print("Crawler created.")
		self.page = requests.get(url)
		self.soup = BeautifulSoup(self.page.content, 'html.parser')

	def print_info(self):
		print(f"URL: {self.page.url}")

	def print_doses(self):
		chart = self.soup.find('table', class_=re.compile("ROATable"))
		print(chart)