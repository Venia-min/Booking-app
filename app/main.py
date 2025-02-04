from fastapi import FastAPI

from app.bookings.router import router as router_bookings
from app.users.router import router as router_users


app = FastAPI()

app.include_router(router_users)
app.include_router(router_bookings)


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
