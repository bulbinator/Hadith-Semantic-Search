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

def semantic_search(query, limit, books):
    vector = model.encode([query])[0].tolist()

    results = collection.aggregate([
        {
            "$vectorSearch": {
                "queryVector": vector,
                "path": "embedding",
                "numCandidates": 1000,
                "limit": limit,
                "index": "VectorSearch",
                "filter": {"book": { "$in": books }}
            }
        },
        {
            "$project": {
                "thaqalaynMatn": 1,
                "book": 1,
                "URL": 1,
                "majlisiGrading": 1,
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
            "hadith": doc['thaqalaynMatn'],
            "similarity_score": doc['score'],
            "book": doc['book'],
            "majlisiGrading": doc['majlisiGrading'],
            "URL": doc['URL']
        })
    return response