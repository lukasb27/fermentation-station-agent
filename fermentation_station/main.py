from fastapi import FastAPI

from fermentation_station.routers import temp, root, last_action

app = FastAPI()

app.include_router(temp.router)
app.include_router(root.router)
app.include_router(last_action.router)
