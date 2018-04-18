import requests, json

api_key= 'KEY'

def news_api_request(api_key, term):
	baseurl= 'https://newsapi.org/v2/everything?q={}&apiKey={}'.format(term, api_key)
	req= requests.get(baseurl)
	return req.json()['articles'][0]

#sample queries
bitcoin= news_api_request(api_key,'bitcoin')
trump= news_api_request(api_key,'trump')
lake= news_api_request(api_key, 'lakes')

#sample use of finding sources' images
source= bitcoin['source']['name']
url= bitcoin['url']
url_image= bitcoin['urlToImage']
#print(url)

#for each term searched, I will create a list in an html template that will return all the previous source 
#images and their corresponding terms


