import streamlit as st

import pandas as pd
import advertools as adv
from advertools import crawl
import logging
from time import time
from collections import Counter
import trafilatura
import string
from wordcloud import WordCloud


site_url = st.text_input('URL to Crawl', '')

if site_url is not None:

	crawl(site_url, 'site_crawl.jl', follow_links=True, custom_settings={'CLOSESPIDER_PAGECOUNT': 3000})
	df = pd.read_json('site_crawl.jl', lines=True)
	df.head()

	urls = df['url'].values.tolist()

	df_url = pd.DataFrame(urls,columns =['urls'])

	result = []


	# Loop items in results
	for page in df_url['urls']:
		downloaded = trafilatura.fetch_url(page)
		if downloaded is not None: # assuming the download was successful
			result.append(trafilatura.extract(downloaded, include_tables=False, include_formatting=False, include_comments=False))
		else:
			result.append("No Text")

	df_url["result"] = result


	#cleaning the text

	df_url['result'] = df_url['result'].astype(str)
	result = ','.join(list(df_url['result'].values))
	result = result.translate(result.maketrans('', '', string.punctuation))
	result = result.lower()


	# Create a WordCloud object
	wordcloud = WordCloud(background_color="white", max_words=5000, contour_width=3, contour_color='steelblue', width=800, height=400)
	#Generate a word cloud
	wordcloud.generate(result)
	# Visualize the word cloud
	wordcloud.to_image()


