# -*- coding: utf-8 -*-

import scraperwiki
import urllib2
from datetime import datetime
from bs4 import BeautifulSoup

# Set up variables
entity_id = "DOH033_DOH_gov"
url = "https://www.gov.uk/government/collections/spending-over-25-000"

# Set up functions
def convert_mth_strings ( mth_string ):
	month_numbers = {'JAN': '01', 'FEB': '02', 'MAR':'03', 'APR':'04', 'MAY':'05', 'JUN':'06', 'JUL':'07', 'AUG':'08', 'SEP':'09','OCT':'10','NOV':'11','DEC':'12' }
	#loop through the months in our dictionary
	for k, v in month_numbers.items():
		#then replace the word with the number
		mth_string = mth_string.replace(k, v)
	return mth_string

# pull down the content from the webpage
html = urllib2.urlopen(url)
soup = BeautifulSoup(html)

# find all entries with the required class
blocks = soup.findAll('li', {'class':'publication document-row'})

for block in blocks:

	link = block.a['href']

	# add the right prefix onto the url
	pageUrl = link.replace("/government","http://www.gov.uk/government")
	
	html2 = urllib2.urlopen(pageUrl)
	soup2 = BeautifulSoup(html2)
	
	fileBlocks = soup2.findAll('div',{'class':'attachment-details'})
	
	for fileBlock in fileBlocks:
		fileUrl = fileBlock.a['href']
		fileUrl = fileUrl.replace("/government","http://www.gov.uk/government")
		fileUrl = fileUrl.replace(".csv/preview",".csv")
		
		title = fileBlock.h2.contents[0]
		titleTest = title.find('Download CSV')
		
		if titleTest == None:
			print 'not a csv'
		else:
			# create the right strings for the new filename
			title = title.upper().strip()
			csvYr = title.split(' ')[-1]
			csvYr = csvYr.replace("200","20")
			
			csvMth = title.split(' ')[-2][:3]
			csvMth = convert_mth_strings(csvMth);
		
			filename = entity_id + "_" + csvYr + "_" + csvMth
		
			todays_date = str(datetime.now())
		
			scraperwiki.sqlite.save(unique_keys=['l'], data={"l": fileUrl, "f": filename, "d": todays_date })
			
			print filename
