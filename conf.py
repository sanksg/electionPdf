from urllib.parse import urljoin

baseUrl = 'http://www.google.com'
detailResultsUrl = urljoin(baseUrl,'detailedResults.html')
laclistUrl = urljoin(baseUrl, 'generalelections', 'lacListAjax.html')

detailedResultsParams = {
  'distNo': "",
  'sEcho':'1', 
  'iColumns':2,
  'sColumns':"",
  'iDisplayStart':0,
  'iDisplayLength':100,
  'iSortingCols':1,
  'iSortCol_0':0,
  'sSortDir_0':'asc',
  'bSortable_0':'false',
  'bSortable_1':'false'
}

sessionHeaders = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Encoding': 'gzip, deflate',
  'Accept-Language': 'en-US,en;q=0.5',
  'Connection': 'keep-alive',
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
}

searchHeaders = {
  "Accept": "application/json, text/javascript, */*",
  "Accept-Encoding": "gzip, deflate",
  "Accept-Language": "en-US,en;q=0.5",
  "Connection": "keep-alive",
  "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
}

outfile = 'keralaVoters.txt'