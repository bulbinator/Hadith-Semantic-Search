import pymongo
import os
import requests
from dotenv import find_dotenv, load_dotenv
from huggingface_hub import InferenceClient

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
DB_PASSWORD = os.getenv("DB_PASSWORD")
HF_TOKEN = os.getenv("HF_TOKEN")
client = pymongo.MongoClient(f"mongodb+srv://smmaisum:{DB_PASSWORD}@hadithsemanticsearch.dky76w8.mongodb.net/?retryWrites=true&w=majority&appName=HadithSemanticSearch")
db = client.hadith
collection = db.all_mpnet


client = InferenceClient(
    provider="hf-inference",
    api_key=HF_TOKEN,
)

def generate_embedding(query):
    result = client.feature_extraction(
    query,
    model="sentence-transformers/all-mpnet-base-v2"
    )
    return result.tolist()



def semantic_search(query, limit, books):
    vector = generate_embedding(query)
    if books == []:
        results = collection.aggregate([
            {
                "$vectorSearch": {
                    "queryVector": vector,
                    "path": "embedding",
                    "numCandidates": 1000,
                    "limit": limit,
                    "index": "VectorSearch",
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

    else:
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