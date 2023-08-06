from functools import reduce
import requests
from bs4 import BeautifulSoup
from requests.api import head

class Crawler:
	def __init__(self, url):
		self.page = requests.get(url)
		self.soup = BeautifulSoup(self.page.content, 'html.parser')

	def print_info(self):
		print(f"URL: {self.page.url}")

	def print_doses(self):
		doses = {}

		# find specific table
		dose_table = self.soup.select_one('table#InfoTable table.ROATable.mw-collapsible tbody')
		substance_title = self.soup.select_one('table#InfoTable tr.SubstanceTitle').text.strip()

		for row in dose_table.find_all('tr', class_="ROASectionRow", limit=6):
			header = row.th.text
			dose = row.td.text
			doses[header] = dose
			
		# Remove this, it isnt a dose.
		# doses.pop("Bioavailability")

		print(f"{substance_title:>0s}".center(50))
		for k, v in doses.items():
			print(f"{k:>0s} : {v:<0s}".center(50).format(k, v))
		
