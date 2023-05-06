import uvicorn
from fastapi import FastAPI

from pages.router import router as router_pages
from lantern.router import router as router_lantern

app = FastAPI(
    title="Lantern App"
)

app.include_router(router_pages)
app.include_router(router_lantern)


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=9999)
