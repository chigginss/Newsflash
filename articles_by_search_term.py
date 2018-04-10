import os
import requests

API_KEY = os.environ['API_KEY']

url = ('https://newsapi.org/v2/top-headlines?q=Apple&sortBy=relevancy&apiKey={}'.format(API_KEY))
response = requests.get(url)
data = response.json()

# url = ('https://newsapi.org/v2/everything?'
#        'q={}&'
#        'from=2018-04-09&'
#        'sortBy=popularity&'
#        'apiKey={}'.format(search_term, API_KEY))

for article in data['articles']:
    description = (article['description'] or " ").encode('utf-8')
    title = (article['title'] or " ").encode('utf-8')
    url = (article['url'] or " ").encode('utf-8')
    author = (article['author'] or " ").encode('utf-8') 
    publishedAt = (article['publishedAt'] or " ").encode('utf-8')
    source = (article['source']['name'] or " ").encode('utf-8')
    urlToImage = (article['urlToImage'] or " ").encode('utf-8')
    print "{}, {}, {}, {}, {}, {}, {}".format(title, url, author, publishedAt, source, description, urlToImage)

