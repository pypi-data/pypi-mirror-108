def search_google(search):
	try:
		from googlesearch import search
	except ImportError:
		return "Sorry unable to search google at the moment. please try agin later."
		
	for j in search(search, tld="co.in", num=10, stop=10, pause=2):
		print(j)

def url_shorten(url):
	import pyshorteners as sh
	s = sh.Shortener()
	return s.tinyurl.short(url)