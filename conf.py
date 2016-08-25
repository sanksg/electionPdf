from urllib.parse import urljoin

baseUrl = 'http://www.ceo.kerala.gov.in'
detailResultsUrl = urljoin(baseUrl,'detailedResultsGE2016.html')
lacListUrl = urljoin(baseUrl, 'generalelections/lacListAjax2016.html')


districtLacParams = {
  'distNo': "",
  'iDisplayStart':'0',
  'iDisplayLength':'1000',
}


searchHeaders = {
  'Accept': 'application/json, text/javascript, */*',
  'Accept-Encoding': 'gzip, deflate, sdch',
  'Accept-Language': 'en-US,en;q=0.5',
  'Connection': 'keep-alive',
  'Content-Type': 'application/x-www-form-urlencoded',
  'DNT': '1',
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'
}

sessionHeaders = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Encoding': 'gzip, deflate',
  'Accept-Language': 'en-US,en;q=0.5',
  'Connection': 'keep-alive',
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'
}


outfile = 'keralaVoters.txt'