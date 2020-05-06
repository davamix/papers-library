"""
This script downloads the papers from arXiv

url_query: configure the query to filter the list of papers to be downloaded
start_at: query parameter usef for pagination
max_results: total papers to be downloaded

Resources
---------
* https://export.arxiv.org/help/api/user-manual#search_query_and_id_list
* https://export.arxiv.org/help/api/user-manual#subject_classifications
"""

import os
import requests
import feedparser
from pathlib import Path
from clint.textui import progress

# Create folder for papers, if not exist
base_path = Path(Path.cwd(), "papers")
if not Path(base_path).exists:
    os.makedirs(base_path)

# Create file index
Path(Path.cwd(), "papers", "index.txt").touch()

url_base = "http://export.arxiv.org/api/query?"
start_at = 500
max_results = 10
url_query = url_base + f"search_query=all:cs&start={start_at}&max_results={max_results}&sortBy=lastUpdatedDate&sortOrder=descending"
print(url_query)

def get_papers(query):
    """
    Execute the query and return the papers metadata

    Parameters
    ----------
    query str: Query to filter the list of papers

    Returns
    -------
    str: Papers metadata from the query
    """
    try:
        response = requests.get(url_query)
        
        return response.text
    except requests.exceptions.HTTPError as e:
        print(f"ERROR: {e.reason}")

        return None

def parse_response(response):
    """
    Return a dictionary with the paper metadata

    Parameters
    ----------
    response str: String that contains the papers metadata

    Returns
    -------
    dict: with all papers metadata
    """
    return feedparser.parse(response)

def generate_file_path(entry):
    """
    Based on the paper ID create the path name where the paper will be downloaded

    Parameters
    ----------
    entry dict: contains the metadata of one paper

    Returns
    -------
    str: file path
    """
    file_name = str(entry["id"].rsplit("/")[-1]) + ".pdf"
    file_path = Path(base_path, file_name)

    return file_path

def extract_link_pdf(entry):
    """
    Get the pdf link from the metadata

    Parameters
    ----------
    entry dict: contains the metadata of one paper

    Returns
    -------
    str: link to pdf
    """
    return [doc["href"] for doc in e["links"] if doc["type"] == "application/pdf"][0]

def download(link, file_path):
    """
    Download the pdf file from the {link}

    Parameters
    -----------
    link str: Link to download the pdf file
    file_path str: path to save the pdf
    """
    try:
        file = requests.get(link, stream=True)

        if file.headers.get('content-length') is None:
            print(f"ERROR: {link} does not exists")
            return

        with open(file_path, "wb") as paper:
            total_length = int(file.headers.get("content-length"))

            for ch in progress.bar(file.iter_content(chunk_size = 1024), expected_size = (total_length / 1024) + 1):
                if ch:
                    paper.write(ch)
                    paper.flush()

    except requests.exceptions.HTTPError as e:
        print(f"ERROR: {e}")


# Get the list of papers (metadata)
papers_list = get_papers(url_query)

if papers_list is not None:
    # Convert the response to dict
    data = parse_response(papers_list)

    # Loop over the list of papers in order to download the pdf files
    for i, e in enumerate(data["entries"]):
        file_path = generate_file_path(e)
        
        link = extract_link_pdf(e)
        
        print(f"[{i+1}/{max_results}] Downloading {link} => {file_path} [{e['title']}]")
        download(link, file_path)