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
collection = db.thaqalayn_api_hadith

model = SentenceTransformer('all-mpnet-base-v2')

query = "Difference between an Imam and a Prophet"
vector = model.encode([query])[0].tolist()

results = collection.aggregate([
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
])

for doc in results:
    print(f"Hadith: {doc['thaqalaynMatn']}\n")
    print(f"Hadith: {doc['book']}\n")