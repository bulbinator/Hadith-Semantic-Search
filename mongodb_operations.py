import pymongo
from pymongo.errors import BulkWriteError
import os
import re
import requests
from dotenv import find_dotenv, load_dotenv
from sentence_transformers import SentenceTransformer

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
DB_PASSWORD = os.getenv("DB_PASSWORD")
client = pymongo.MongoClient(f"mongodb+srv://smmaisum:{DB_PASSWORD}@hadithsemanticsearch.dky76w8.mongodb.net/?retryWrites=true&w=majority&appName=HadithSemanticSearch")
db = client.hadith
collection = db.all_mpnet

response = requests.get('https://www.thaqalayn-api.net/api/v2/allbooks')
books = response.json()
book_ids = [book['bookId'] for book in books if book['bookId'] != 'Kitab-al-Duafa-Ghadairi']

all_hadiths = []
model = SentenceTransformer('all-mpnet-base-v2')

for id in book_ids:
    url = f"https://www.thaqalayn-api.net/api/v2/{id}"
    response = requests.get(url)
    hadiths = response.json()

    for hadith in hadiths:
        grading = re.search(r'[\u0600-\u06FF]+', hadith['majlisiGrading'])
        if grading:
            hadith['majlisiGrading'] = grading.group(0)

        all_hadiths.append(
            {
                'thaqalaynMatn': hadith['thaqalaynMatn'],
                'thaqalaynSanad': hadith['thaqalaynSanad'],
                'majlisiGrading': hadith['majlisiGrading'],
                'book': hadith['book'],
                'author': hadith['author'],
                'chapter': hadith['chapter'],
                'URL': hadith['URL'],
                'embedding': model.encode(hadith['thaqalaynMatn']).tolist()
            }
        )

def insert_in_chunks(docs, chunk_size=100):
    for i in range(0, len(docs), chunk_size):
        try:
            collection.insert_many(docs[i:i + chunk_size])
            print(f"Inserted chunk {i // chunk_size + 1}")
        except BulkWriteError as bwe:
            print(f"Bulk write error: {bwe.details}")
        except Exception as e:
            print(f"Failed on chunk {i // chunk_size + 1}: {e}")


insert_in_chunks(all_hadiths, chunk_size=100)