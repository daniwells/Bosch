from fastapi import FastAPI, HTTPException, status, Depends
from model import Futball
from typing import Optional, Any

app = FastAPI(title="JVL API", version="0.0.1", description="A api made in Joinville")

teams = {
    1: {
        "name_team": "Athletico Paranaense",
        "date_foundation": "21/03/1924",
        "qtd_champions": 200,
        "stage": "Ligga Arena",
    },
    2: {
        "name_team": "Corinthians",
        "date_foundation": "01/09/1910",
        "qtd_champions": 54,
        "stage": "Neo Quimica Arena",
    },
}

def fake_db():
    try:
        print("Conected")
    finally:
        print("Close Connection")


@app.get("/")
async def raiz():
    return {"message": "It's ok"}


@app.get("/teams")
async def get_teams(db: Any = Depends(fake_db)):
    return teams


@app.get("/teams/{id_team}")
async def get_team(id_team: int):
    try:
        team = teams[id_team]
        return team
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teams Not found")


@app.post("/teams", status_code=status.HTTP_201_CREATED)
async def post_teams(team: Optional[Futball] = None):
    next_id = len(teams) + 1
    teams[next_id] = team
    del team.id
    return team


@app.put("/teams/{id_team}")
async def put_team(id_team: int, team: Futball):
    if id_team in teams:
        teams[id_team] = team
        team.id = id_team
        return team
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There aren't a team with ID {id_team}")


@app.delete("/teams/{id_team}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(id_team: int):
    if id_team in teams:
        del teams[id_team]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There aren't a team with ID {id_team}")


if __name__ == "__main__":
    import uvicorn 
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)