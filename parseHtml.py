from bs4 import BeautifulSoup as BS

data = []
with open("details.html", 'r') as htmlFile:
  soup = BS(htmlFile, 'html.parser')
  tables = soup.find_all('table')
  for table in tables:
    rows = table.find_all('tr')
    for row in rows:
      cols = row.find_all('td')
      cols = [ele.text.strip() for ele in cols]
      parsedRow = [ele for ele in cols if len(ele)>0]
      print ">> ",parsedRow
      data.append(parsedRow)

print data

