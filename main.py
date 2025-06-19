import pymongo
import os
import requests
from dotenv import find_dotenv, load_dotenv
from sentence_transformers import SentenceTransformer

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
DB_PASSWORD = os.getenv("DB_PASSWORD")
client = pymongo.MongoClient(f"mongodb+srv://smmaisum:{DB_PASSWORD}@hadithsemanticsearch.dky76w8.mongodb.net/?retryWrites=true&w=majority&appName=HadithSemanticSearch")
db = client.hadith
collection = db.all_mpnet

model = SentenceTransformer('all-mpnet-base-v2')

def semantic_search(query, limit):
    vector = model.encode([query])[0].tolist()

    results = collection.aggregate([
        {
            "$vectorSearch": {
                "queryVector": vector,
                "path": "embedding",
                "numCandidates": 1000,
                "limit": limit,
                "index": "VectorSearch"
            }
        },
        {
            "$project": {
                "thaqalaynMatn": 1,
                "book": 1,
                "score": { "$meta": "vectorSearchScore" }
            }
        }
    ])

    """results = collection.aggregate([
        {
            "$vectorSearch": {
                "queryVector": vector,
                "path": "embedding",
                "numCandidates": 100,
                "limit": 5,
                "index": "VectorSearch",
                "filter": {
                    "book": {"$eq": "Al-Amālī"}
                }
            }
        }
    ])"""

    response = []
    for doc in results:
        response.append({
            "score": doc['score'],
            "book": doc['book'],
            "hadith": doc['thaqalaynMatn'],
        })