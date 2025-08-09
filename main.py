from fastapi import FastAPI
from database import Base, engine
from auth import views as a_view
from blog import views as b_view
from reviews import views as r_view

app = FastAPI(
    title="Blog Api",
    description="Blog Api with user authentication",
    version="0.1"
)

Base.metadata.create_all(bind=engine)

@app.get("/")
async def check_api():
    return {
        "detail" : "Working Fine"
    }
    
app.include_router(a_view.router)
app.include_router(b_view.router)
app.include_router(r_view.router)