
from bs4 import BeautifulSoup
import re
import requests
import slate
import csv
import urllib

# hitting the ffiec website with a "get" request
r = requests.get("https://www.ffiec.gov/nicpubweb/content/BHCPRRPT/BHCPR_Peer.htm")
# saving response
html_doc = r.text
# parsing the page using BeautifulSoup module
soup = BeautifulSoup(html_doc, 'html.parser')
# reading div tag of our interest
mydivs = soup.find_all("div",{'class':'contentfull'})
# list to save link of all peer 1 files
list_of_links = []
# "for loop" to read all links
for tables in mydivs[0].findAll('table') :
	# reading all rows 
    rows = tables.findAll("tr")
    # reading all cells with links
    links  = rows[1].findAll("td")
    # for loop to save all links in a list
    for link in links:
    	# "if condition" to check whether a link is empty
        if(link.a != None):
        	# saving links into a list
            list_of_links.append("https://www.ffiec.gov/nicpubweb/content/BHCPRRPT/" + link.a.get('href'))

# traversing the above list i.e. all PDF files to scrape into a CSV
for linked_file in list_of_links:
	# fetching file from the link
	response = urllib.urlopen(linked_file)
	# opening file
	pdf_file = open("document.pdf","wb")
	# reading the file
	pdf_file.write(response.read())
	pdf_file.close()
	# a list to save all lines from the file
	records =[]
	# opening the PDF file
	with open("document.pdf","rb") as f:
		# scraping the PDF file
		doc = slate.PDF(f)
	# reading the PDF file page wise
	for pages in doc:
		# splitting all lines
 		z = re.split("\n",pages.strip())
 		# saving all lines of data in a list
		records.append([x for x in z if x])
	# final list to save all rows and columns i.e. all data in tabular format
	final_list =[]
	# traversing all the lines separated above
	for record in records:
		# traversing data in each line
		for r in record:
			# splitting the data in each line of PDF
			y = re.split(r"\s{2,}",r.strip())
			# saving all data cells in a list if it is not empty data
			final_list.append([x for x in y if x])
	# reading the quarter & year of the file
	index = linked_file.find("_1_")
	# file name in string format as requested i.e. Peer1_Year_Quarter.csv
	file_name = "Peer1_"+linked_file[-8:-4]+"_"+linked_file[index+3:-8]+".csv"
	# creating an empty CSV file
	with open(file_name,"wb") as o:
		# initializing the writer
		writer = csv.writer(o)
		# writing the data into the CSV file
		writer.writerows(final_list)