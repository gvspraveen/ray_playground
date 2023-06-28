from anyscale_docs_crawler import scrape_urls
from llama_index import SimpleWebPageReader
# Inspired by https://www.anyscale.com/blog/build-and-scale-a-powerful-query-engine-with-llamaindex-ray

urls = list(scrape_urls())
documents = SimpleWebPageReader(html_to_text=True).load_data(urls[0:1])
print(documents[0])