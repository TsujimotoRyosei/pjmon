from fastapi import FastAPI, Request, Form, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from danjon import playerpm, monsterbox, battle
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="mon/templates")

game_state = {"player_data": None, "monster_data": None, "initial_appearance": True}

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/player_status", response_class=HTMLResponse)
async def player_status(request: Request, username: str = Form(...)):
    game_state["player_data"] = playerpm()
    game_state["player_data"][0] = username
    player_data = {"username": username, 
                   "level": game_state["player_data"][1],
                   "hp": game_state["player_data"][2], 
                   "mp": game_state["player_data"][4]}
    return templates.TemplateResponse("home.html", {"request": request, "player": player_data})

@app.post("/start_game", response_class=HTMLResponse)
async def start_game(request: Request):
    game_state["monster_data"], game_state["player_data"] = monsterbox(game_state["player_data"])
    game_state["initial_appearance"] = True  # 初回のモンスター出現時のみTrue
    monster_data = {"name": game_state["monster_data"][0], 
                    "hp": game_state["monster_data"][1]}
    return templates.TemplateResponse("battle.html", {"request": request, "player": game_state["player_data"], "monster": monster_data, "initial_appearance": game_state["initial_appearance"]})

@app.get("/battle_action", response_class=JSONResponse)
async def battle_action(request: Request, action: str = Query(...)):
    if game_state["monster_data"] is None:
        return JSONResponse({"result": "新しいモンスターを生成する必要があります。"}, status_code=400)

    result, updated_data = battle(game_state["monster_data"], game_state["player_data"], action)
    game_state["monster_data"], game_state["player_data"] = updated_data

    # モンスターが倒された場合、HPを None として返す
    monster_data = {
        "name": game_state["monster_data"][0] if game_state["monster_data"] else None,
        "hp": game_state["monster_data"][1] if game_state["monster_data"] else None
    }
    player_data = {
        "hp": game_state["player_data"][2],
        "mp": game_state["player_data"][4]
    }

    return {"result": result, "monster": monster_data, "player": player_data}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
