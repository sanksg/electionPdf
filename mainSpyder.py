import conf
import datetime, time
import string

from scraper import Scraper



def main():

#  while datetime.datetime.now().time() < datetime.time(2, 30):
#    print "Sleeping for 300 secs"
#    time.sleep(300)
  print( "== Starting Script ==")
  startTime = datetime.datetime.now()
  
  conf.searchParams['distNo'] = 8
  conf.searchParams['lacNo'] = 75

  # Cycle through the starting letters 
  letterArray = string.ascii_lowercase
  
  for letter in letterArray:
    start_threads_for_letter(letter)
    
  endtime = datetime.datetime.now()
  
  print("Script running time : %f seconds" % (endtime - startTime).total_seconds())

  
  
def start_threads_for_letter(startLetter):
  outFn = "voters_"+str(startLetter)+".txt"
  outFile = open(outFn, 'w')
  
  print("Getting records starting with " + startLetter)

  scp = Scraper(conf.sessionHeaders, conf.searchHeaders)
  scp.setup_session([conf.baseUrl, conf.rollSearchUrl])
 
  url = conf.searchUrl
  params = conf.searchParams

  params['electorName'] = startLetter

  scp.get_and_write_records(url, 0, params, outFile)
  
  
  
if __name__ == "__main__":
  # execute only if run as a script
  main()

