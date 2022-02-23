import streamlit as st

import pandas as pd
import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession
import trafilatura
import string
from wordcloud import WordCloud


#Scraping Title, Link and Text

def get_results(query):
    
    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.com/search?q=" + query)
    
    return response


def parse_results(response):
    
    css_identifier_result = ".tF2Cxc"
    css_identifier_title = "h3"
    css_identifier_link = ".yuRUbf a"
    css_identifier_text = ".IsZvec"
    
    results = response.html.find(css_identifier_result)

    output = []
    
    for result in results:

        item = {
            'title': result.find(css_identifier_title, first=True).text,
            'link': result.find(css_identifier_link, first=True).attrs['href'],
        }
        
        output.append(item)
        
    return output

def google_search(query):
    response = get_results(query)
    return parse_results(response)


def get_source(url):
    try:
        session = HTMLSession()
        response = session.get(url)
        return response 
    except requests.exceptions.RequestException as e:
        print(e)    


query = st.text_input('Query', '')

results = google_search(query)

#Your Indexed Pages


df = pd.DataFrame(results)

content = []

# Loop items in results
for page in df['link']:
  downloaded = trafilatura.fetch_url(page)
  if downloaded is not None: # assuming the download was successful
    content.append(trafilatura.extract(downloaded, include_tables=False, include_formatting=False, include_comments=False))
  else:
    content.append("No Text")

df["content"] = content

st.dataframe(df)

#Analysing the SERPs

df['content'] = df['content'].astype(str)

text = ','.join(list(df['content'].values))
text = text.translate(text.maketrans('', '', string.punctuation))
text = text.lower()

#Word Cloud

# Import the wordcloud library
from wordcloud import WordCloud

# Create a WordCloud object
wordcloud = WordCloud(background_color="white", max_words=5000, contour_width=3, contour_color='steelblue', width=800, height=400)
# Generate a word cloud
wordcloud.generate(text)
# Visualize the word cloud
wordcloud.to_image()
