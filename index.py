import urllib, urllib.request
from xml.dom.minidom import parse
import xml.dom.minidom
import sys
from pdf2image import convert_from_path
import os
from PIL import Image
import pytesseract

def convertToText(title):
    PDF_file = title + '.pdf'
    outfile = title + '.txt'
    '''
    Part #1 : Converting PDF to images
    '''

    # Store all the pages of the PDF in a variable
    pages = convert_from_path(PDF_file, 500)

    # Counter to store images of each page of PDF to image
    image_counter = 1

    # Iterate through all the pages stored above
    for page in pages:
        filename = title + "_page_"+str(image_counter)+".jpg"

    # Save the image of the page in system
        page.save(filename, 'JPEG')

    # Increment the counter to update filename
        image_counter = image_counter + 1

    '''
    Part #2 - Recognizing text from the images using OCR
    '''
    # Variable to get count of total number of pages
    filelimit = image_counter-1

    # Open the file in append mode so that
    # All contents of all images are added to the same file
    f = open(outfile, "a")

    # Iterate from 1 to total number of pages
    for i in range(1, filelimit + 1):
        filename = title + "_page_"+str(i)+".jpg"

    # Recognize the text as string in image using pytesserct
        text = str(((pytesseract.image_to_string(Image.open(filename)))))

    # The recognized text is stored in variable text
    # Any string processing may be applied on text
    # Here, basic formatting has been done:
    # In many PDFs, at line ending, if a word can't
    # be written fully, a 'hyphen' is added.
    # The rest of the word is written in the next line
    # Eg: This is a sample text this word here GeeksF-
    # orGeeks is half on first line, remaining on next.
    # To remove this, we replace every '-\n' to ''.
        text = text.replace('-\n', '')

    # Finally, write the processed text to the file.
        f.write(text)
        os.remove(filename)
    # Close the file after writing all the text.
    f.close()

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
   title = title.replace(" ", "_")
   pdfTitle = title + '.pdf'

   outfile = title + '.txt'
   urllib.request.urlretrieve(pdf, pdfTitle)
   convertToText(title)
   print("\n")


print("Done downloading...")