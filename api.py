from fastapi import FastAPI, Query
from typing import Optional, List, Literal
from fastapi.responses import JSONResponse
from main import semantic_search
import requests

BookName = Literal['Al-Amālī', 'Al-Amālī', 'Al-Kāfi - Volume 1', 'Al-Kāfi - Volume 2', 'Al-Kāfi - Volume 3', 'Al-Kāfi - Volume 4', 'Al-Kāfi - Volume 5', 'Al-Kāfi - Volume 6', 'Al-Kāfi - Volume 7', 'Al-Kāfi - Volume 8', 'Al-Khiṣāl', 'Al-Tawḥīd', 'Faḍaʾil al-Shīʿa', 'Kāmil al-Ziyārāt', 'Kitāb al-Ḍuʿafāʾ', 'Kitāb al-Ghayba', 'Kitāb al-Ghayba', 'Kitāb al-Muʾmin', 'Kitāb al-Zuhd', 'Maʿānī al-ʾAkhbār', 'Muʿjam al-Aḥādīth al-Muʿtabara', 'Nahj al-Balāgha', 'Risālat al-Ḥuqūq', 'Ṣifāt al-Shīʿa', 'Thawāb al-Aʿmāl wa ʿiqāb al-Aʿmāl', 'ʿUyūn akhbār al-Riḍā - Volume 1', 'ʿUyūn akhbār al-Riḍā - Volume 2']

# Create FastAPI app
app = FastAPI(
    title="Hadith Semantic Search",
    version="1.0.0"
)

# Search endpoint
@app.get("/search")
async def search(query: str = Query(..., description="Enter your search query"),
                 limit: int = Query(5, description="Number of results to return"),
                 books: Optional[List[BookName]] = Query(None, description="Filter by books (multiple allowed)")):
    response = semantic_search(query, limit, books)
    print(response)
    return JSONResponse(content=response)
