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
#  print(resp.text)
  
  
  #Parse the html with bs4 using the "html.parser"
  soup = BS(resp.text, 'html.parser')
  options = soup.find_all(id='distNo', name='distNo')
  if len(options) == 0:
    print("ERROR: Could not find tag with id=distNo in html for url ", resp.url)
    exit(0)
  for option in options.find_all('option'):
    print(option.value)
    
  endtime = datetime.datetime.now()
  
  print("Script running time : %f seconds" % (endtime - startTime).total_seconds())


  
if __name__ == "__main__":
  # execute only if run as a script
  main()

