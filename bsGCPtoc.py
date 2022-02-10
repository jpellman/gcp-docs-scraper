#!/usr/bin/env python
from bs4 import BeautifulSoup
from urllib.request import urlopen
from collections import OrderedDict

services = [ 
	"/compute/docs/instances", \
	"/iam/docs/understanding-simulator", \
	"/vpc/docs/vpc", \
	"/storage/docs/creating-buckets", \
	"/kubernetes-engine/docs/concepts/kubernetes-engine-overview"]

for service in services:
	with urlopen("https://cloud.google.com%s" % service) as response:
		service = service.split('/')[1]
		soup = BeautifulSoup(response, 'html.parser')
		book = soup.find("ul", menu="_book")
		docDict = OrderedDict()
		for i in book.find_all(['li']):
			lc = i.get('class')
			if "devsite-nav-heading" not in lc:
				cText = None
				a = None
				c = None
				for j in i.find_all('a'):
					a = j.get('href')
					c = i.find('span')
					if c:
						cText = c.get_text().strip()
					if cText and a:
						if a.startswith("/%s" % service):
							docDict[cText] = a
						c = None
						cText = None
						a = None
	with open("%s.csv" % service, "w") as f:
		for k,v in docDict.items():
			f.write("%s;https://cloud.google.com%s\n" % (k,v))			

