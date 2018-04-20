import os
import requests

API_KEY = os.environ['API_KEY']


# url = ('https://newsapi.org/v2/top-headlines?language=en&q=Trump&sources=google-news&sortBy=relevancy&apiKey={}'.format(API_KEY))
# url = ('https://newsapi.org/v2/top-headlines?language=en&q=Trump&sortBy=relevancy&apiKey={}'.format(API_KEY))

def articles_by_search():
    # url = ('https://newsapi.org/v2/top-headlines?language=en&q=Google&sources=google-news&sortBy=relevancy&apiKey={}'.format(API_KEY))
    url = ('https://newsapi.org/v2/top-headlines?language=en&q={}&sortBy=relevancy&apiKey={}'.format({{ keyword }}, API_KEY))
    response = requests.get(url)
    data = response.json()

    # for article in data['articles']:
    #     description = (article['description'] or " ").encode('utf-8')
    #     title = (article['title'] or " ").encode('utf-8')
    #     url = (article['url'] or " ").encode('utf-8')
    #     author = (article['author'] or " ").encode('utf-8') 
    #     publishedAt = (article['publishedAt'] or " ").encode('utf-8')
    #     source = (article['source']['name'] or " ").encode('utf-8')
    #     urlToImage = (article['urlToImage'] or " ").encode('utf-8')
    #     print "{}, {}, {}, {}, {}, {}, {}".format(title, url, author, publishedAt, source, description, urlToImage)
    print data
    return data

    result = return_top_headlines()