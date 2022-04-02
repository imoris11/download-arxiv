import urllib, urllib.request
from xml.dom.minidom import parse
import xml.dom.minidom
import sys

term = str(sys.argv[1])
limit = 10

if(str(sys.argv[2])):
    limit = str(sys.argv[2])

url = 'http://export.arxiv.org/api/query?search_query=all:'+term+'&start=0&max_results='+limit
data = urllib.request.urlopen(url)
formatted = data.read().decode('UTF-8')

# Open XML document using minidom parser
with open('papers.xml', 'wb') as f:
    f.write(formatted.encode())


DOMTree = xml.dom.minidom.parse('papers.xml')
collection = DOMTree.documentElement

# Get all the movies in the collection
entries = collection.getElementsByTagName("entry")


for entry in entries:
   print("*****Entry*****")
   title = entry.getElementsByTagName('title')[0]
   print ("Downloading: %s" % title.childNodes[0].data)
   summary = entry.getElementsByTagName('summary')[0]
   print ("Summary: %s" % summary.childNodes[0].data)
   author = entry.getElementsByTagName('name')[0]
   print( "Author: %s" % author.childNodes[0].data)
   fileLink = entry.getElementsByTagName('link')[1]
   print ("Link: %s" % fileLink.getAttribute('href'))
   # Download PDF
   link = fileLink.getAttribute('href')
   pdf = link + '.pdf'
   title = title.childNodes[0].data
   pdfTitle = title + '.pdf'
   urllib.request.urlretrieve(pdf, pdfTitle)
   print("\n")


print("Done downloading...")
   

