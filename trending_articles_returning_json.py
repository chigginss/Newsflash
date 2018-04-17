
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

    print data
    return data

# for article in data['articles']:
#     description = (article['description'] or " ").encode('utf-8')
#     title = (article['title'] or " ").encode('utf-8')
#     url = (article['url'] or " ").encode('utf-8')
#     author = (article['author'] or " ").encode('utf-8') 
#     publishedAt = (article['publishedAt'] or " ").encode('utf-8')
#     source = (article['source']['name'] or " ").encode('utf-8')
#     # bias = 
#     # popularity =
#     urlToImage = (article['urlToImage'] or " ").encode('utf-8')
#     print "{}, {}, {}, {}, {}, {}, {}".format(title, url, author, publishedAt, source, description, urlToImage)


result = return_top_headlines()