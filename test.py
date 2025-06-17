import requests
import re

url = f"https://www.thaqalayn-api.net/api/v2/Al-Kafi-Volume-1-Kulayni"
response = requests.get(url)
hadiths = response.json()

all_hadiths = []

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
        }
    )

print(all_hadiths[:5])