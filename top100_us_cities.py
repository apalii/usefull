import requests
from bs4 import BeautifulSoup as bs
import re

page = requests.get('http://www.citymayors.com/gratis/uscities_100.html')
soup = bs(page.text)

# Get cities
cities = []
for i in soup.find_all('font'):
    i = i.text
    if re.match(r'^.+;\W\w+', i) or re.match(r'^A|G.+,\W\w+', i):
        cities.append(i.replace(',', ';'))
cities.remove('City; State')

# Get statistics
soup = bs(page.text)
res = []
table = bs(str(soup.findAll('table', {'width':'433'})[0]))
for i in table.findAll('div', {'align':'right'}):
    line = i.get_text().strip()
    res.append(line)
    
def three_elements(some_iter):
    return some_iter.next(),some_iter.next(),some_iter.next()

my_iter = iter(res)
count = 0
q = ['Rank',
 'City; State',
 '2010 population',
 '2012 population',
 'Growth/Decline']

print "{:<4} | {:<33}| {:<16}| {:<16}| {:<15} |".format(q[0].center(4),
                                                       q[1].center(33),
                                                       q[2].center(16),
                                                       q[3].center(16),
                                                       q[4].center(15))
for city in cities:
    z,x,c = three_elements(my_iter)
    count += 1
    print "{:<4} | {:<33}| {:<16}| {:<16}| {:<15} |".format(count, city, z, x, c)
