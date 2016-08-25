import conf
import datetime, time
import string

from scraper import Scraper
from bs4 import BeautifulSoup as BS



def main():

#  while datetime.datetime.now().time() < datetime.time(2, 30):
#    print "Sleeping for 300 secs"
#    time.sleep(300)
  print( "== Starting Download ==")
  startTime = datetime.datetime.now()
  
  #Get the detailedResults page
  scp = Scraper(conf.sessionHeaders, conf.searchHeaders, [conf.baseUrl])
  scp.setup_session()
  resp = scp.get_response(conf.detailResultsUrl, '', 1)
#  print(resp.text.encode('utf8'))
  
  page = resp.text
##  page = open('detailedResults.html', 'r')

  #Parse the html with bs4 using the "html.parser"
  soup = BS(page, 'html.parser')
  
  #Process the HTML to find the District dropdown list
  options = soup.find_all(id='distNo')[0]
  if len(options) == 0:
    print("ERROR: Could not find tag with id=distNo in html for url ", resp.url)
    exit(0)
  #Go through each option in the district dropdown to get the LACs
  for option in options.find_all('option'):
    optVal = option['value']
    if optVal =="":
      continue
    
    #Get the LAC list page for this district with all the PDF links
    conf.districtLacParams['distNo'] = str(optVal)
    lacListPage = scp.get_json_response(conf.lacListUrl, conf.districtLacParams, 1 )
    
    #Create a key file for mapping LAC names to filename
    keyf = open("lacFileKey.txt", "w+")
    
    #Download each file in the LAC link list
    for lac in lacListPage['aaData']:
      link = BS(lac[1], "html.parser").a['href']
      lacName = lac[0]
      fileName = link.split('/')[-1]
      keyf.write("{},{}{}".format(lacName, fileName, "\n"))
      scp.downloadFile(link, fileName)
      time.sleep(2)

    
  endtime = datetime.datetime.now()
  
  print("Script running time : %f seconds" % (endtime - startTime).total_seconds())


  
if __name__ == "__main__":
  # execute only if run as a script
  main()

