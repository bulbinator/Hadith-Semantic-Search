from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from main import semantic_search

# Create FastAPI app
app = FastAPI(
    title="Hadith Semantic Search",
    version="1.0.0"
)

# Search endpoint
@app.get("/search")
async def search(query: str = Query(..., description="Enter your search query"),
                 limit: int = Query(5, description="Number of results to return")):
    response = semantic_search(query, limit)
    print(response)
    return JSONResponse(content=response)

# Run with: uvicorn api:app --reload
