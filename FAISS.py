from sentence_transformers import SentenceTransformer
import requests
import json
import faiss
import numpy as np
from sklearn.preprocessing import normalize


response = requests.get('https://www.thaqalayn-api.net/api/v2/Al-Kafi-Volume-1-Kulayni')
response = response.json()
hadiths = [hadith['thaqalaynMatn'] for hadith in response]

model = SentenceTransformer('all-MiniLM-L6-v2')  # Small and fast, good enough for most cases
hadith_embeddings = model.encode(hadiths, convert_to_tensor=True)

# Step 4: Build FAISS index
dimension = hadith_embeddings[0].shape[0]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(hadith_embeddings))


def search(query, top_k=5):
    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding), top_k)
    results = [response[i]['thaqalaynMatn'] for i in I[0]]
    for result in results:
        print(result)

# Try it
results = search("Difference between an Imam and a Prophet")