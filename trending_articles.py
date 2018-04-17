
# import newsapi
import os
import requests
# from sys import argv
# from pprint import pprint
# import json

API_KEY = os.environ['API_KEY']
# api = newsapi.NewsApiClient(api_key=API_KEY)

# top_headlines = api.get_everything(q='bitcoin',
#                                    language='en')

# url = ('https://newsapi.org/v2/top-headlines?language=en&from=2018-04-09&sortBy=popularity&apiKey={}'.format(API_KEY))
# url = ('https://newsapi.org/v2/top-headlines?language=en&pageSize=50&from=2018-04-09&sortBy=popularity&apiKey={}'.format(API_KEY))
# url = ('https://newsapi.org/v2/top-headlines?language=en&pageSize=50&apiKey={}'.format(API_KEY))
# url = ('https://newsapi.org/v2/top-headlines?language=en&sources=google-news&apiKey={}'.format(API_KEY))
# url = ('https://newsapi.org/v2/top-headlines?language=en&sortBy=popularity&apiKey={}'.format(API_KEY))

# print top_headlines
def return_top_headlines():
    """Pull top trending articles from News API"""
# url = ('https://newsapi.org/v2/top-headlines?language=en&sources=google-news&apiKey={}'.format(API_KEY))
url = ('https://newsapi.org/v2/top-headlines?sources=the-wall-street-journal,the-new-york-times,bbc-news,techcrunch,the-washington-post,cnn,fox-news,breitbart-news,time,wired,business-insider,usa-today,politico,cnbc,engadget,nbc-news,cbs-news,abc-news,associated-press,fortune&apiKey={}'.format(API_KEY))
response = requests.get(url)
data = response.json()

# print data

for article in data['articles']:
    description = (article['description'] or " ").encode('utf-8')
    title = (article['title'] or " ").encode('utf-8')
    url = (article['url'] or " ").encode('utf-8')
    author = (article['author'] or " ").encode('utf-8') 
    publishedAt = (article['publishedAt'] or " ").encode('utf-8')
    source = (article['source']['name'] or " ").encode('utf-8')
    # bias = 
    # popularity =
    urlToImage = (article['urlToImage'] or " ").encode('utf-8')
    print "{}, {}, {}, {}, {}, {}, {}".format(title, url, author, publishedAt, source, description, urlToImage)


# for articles in data['articles']:
#     description = data['articles'][1].get('description')
#     title = data['articles'][3].get('title')
#     url = data['articles'][5].get('url')
#     author = data['articles'][7].get('author')
#     publishedAt = data['articles'][9].get('publishedAt')
#     source = data['articles'][11].get('source')
#     urlToImage = data['articles'][13].get('urlToImage')
#     print "%s, %s, %s, %s, %s, %s, %s" % (title, url, author, publishedAt, source, description, urlToImage)
#     # print "%s" % (title)



# { u'description': u'Ms. Duckworth gave birth to a daughter, Maile, on Monday. She is one of 10 women to give birth while serving in Congress, and the first senator to do so.',
#   u'title': u'Tammy Duckworth Becomes First Sitting US Senator to Give Birth', 
#   u'url': u'https://www.nytimes.com/2018/04/09/us/politics/tammy-duckworth-birth.html',
#   u'author': u'Liam Stack', 
#   u'publishedAt': u'2018-04-09T20:05:42Z', 
#   u'source': {u'id': u'the-new-york-times', u'name': u'The New York Times'}, 
#   u'urlToImage': u'https://static01.nyt.com/images/2018/04/10/autossell/10XP-DUCKWORTH/10XP-DUCKWORTH-facebookJumbo.jpg'}
