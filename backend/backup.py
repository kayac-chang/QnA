# pretty the output
from rich import pretty, print
from rich.markdown import Markdown

pretty.install()


# debug mode
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# download the article
from requests import get

url = "https://gogoout.com/blog/okinawa-tour/"
response = get(url)

# parse the article into markdown
from bs4 import BeautifulSoup
from markdownify import markdownify as md

soup = BeautifulSoup(response.text, "html.parser")
article = soup.find("article")
text = md(str(article))

from ai.create_index import create_vector_index_from_text

index = create_vector_index_from_text(text)
retriever = index.as_retriever()

for node in retriever.retrieve("沖繩自由行安排?"):
    print(Markdown(node.text))
