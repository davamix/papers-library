from pymongo import MongoClient
from bson.json_util import dumps

class DatabaseService():
    def __init__(self):
        client = MongoClient("mongodb://mongodb:27017")
        self.database = client.papers_db
        

    def save(self, data):
        return self.database.papers_collection.insert_one(data).inserted_id

    def get_paper(self, paper_id):
        """
        Get the papers based on the paper_id

        Parameters:
            paper_id str: Paper Arxiv ID 

        Returns:
            The paper data if paper_id exists, otherwise returns None
        """
        paper = self.database.papers_collection.find_one({"paper_id": paper_id})

        if paper is not None:
            return dumps(paper)

        return None

    def get_papers(self, filter = {}):
        """
        Get a list the the papers that match with the filter

        Parameters:
            filter dict: Dictionary with the property and values used to filter the data

        Returns:
            List of papers that match with the filter
        """
        papers = list(self.database.papers_collection.find(filter))
        
        return dumps(papers)