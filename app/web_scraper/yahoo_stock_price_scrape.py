import urllib2
import pprint

response = urllib2.urlopen('http://finance.yahoo.com/q/ks?s=VHT')

response = urllib2.urlopen("http://finance.yahoo.com/quote/")

a = response.read(50000)
pprint.pprint(a)
