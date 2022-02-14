#!/usr/bin/env python
from bs4 import BeautifulSoup
from bs4.element import Tag
from urllib.request import urlopen
from collections import OrderedDict
import os

services = [ 
	"/compute/docs/instances", \
	"/iam/docs/understanding-simulator", \
	"/vpc/docs/vpc", \
	"/storage/docs/creating-buckets", \
	"/kubernetes-engine/docs/concepts/kubernetes-engine-overview"]

os.makedirs('csvs', exist_ok=True)
for service in services:
	with urlopen("https://cloud.google.com%s" % service) as response:
		service = service.split('/')[1]
		soup = BeautifulSoup(response, 'html.parser')
		book = soup.find("ul", menu="_book")
		docDict = OrderedDict()
		for i in book.find_all(['li']):
			lc = i.get('class')
			if "devsite-nav-heading" not in lc:
				a = None
				s = None
				sText = None
				for j in i.find_all('a'):
					a = j.get('href')
					s = i.find('span')
					if s:
						sText = s.get_text().strip()
					if sText and a:
						if a.startswith("/%s" % service):
							docDict[sText] = a
						s = None
						sText = None
						a = None
	with open("csvs/%s.csv" % service, "w") as f:
		for k,v in docDict.items():
			f.write("%s;https://cloud.google.com%s\n" % (k,v))			
	os.makedirs(service, exist_ok=True)
	for idx,v in enumerate(docDict.values()):
		with urlopen("https://cloud.google.com%s" % v) as response:
			soup = BeautifulSoup(response, 'html.parser')
		with open("%s/%.4d.html" % (service, idx),"w") as f:
			f.write(str(soup.head))
			f.write("<body>\n")
			for i in soup.article.contents:
				if isinstance(i,Tag):	
					if "class" in i.attrs:
						if "nocontent" in i["class"]:
							continue
						# Fix images to use absolute paths
						if "devsite-article-body" in i["class"]:
							imgs = i.find_all("img")
							for img in imgs:
								if img["src"].startswith("/"):
									img["src"] = "https://cloud.google.com%s" % img["src"]
					if "data-label" in i.attrs:
						if i["data-label"] == "Send Feedback Button":
							continue
					f.write(str(i))
				else:
					f.write(str(i))
			f.write("</body>\n")
