from fastapi import FastAPI, Request, Form, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from danjon import playerpm, monsterbox, battle
import uvicorn
import random

app = FastAPI()
templates = Jinja2Templates(directory="mon/templates")

app.mount("/monster_images", StaticFiles(directory="mon/monster_images"), name="monster_images")

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
    game_state["initial_appearance"] = True
    monster_data = {"name": game_state["monster_data"][0], 
                    "hp": game_state["monster_data"][1]}
    monster_image = get_monster_image_path(game_state["monster_data"][0])
    return templates.TemplateResponse("battle.html", {"request": request, "player": game_state["player_data"], "monster": monster_data, "initial_appearance": game_state["initial_appearance"], "monster_image": f"/monster_images/{monster_image}"})

def get_monster_image_path(monster_name):
    if monster_name == "スライム":
        return random.choice(["slime/slime1.jpeg", "slime/slime2.jpeg"])
    elif monster_name == "ゴブリン":
        return random.choice(["goblin/goblin1.jpeg", "goblin/goblin2.jpeg"])
    elif monster_name == "オーク":
        return random.choice(["orc/orc1.jpeg", "orc/orc2.jpeg"])
    elif monster_name == "ドラゴン":
        return random.choice(["dragon/dragon1.jpeg", "dragon/dragon2.jpeg"])

@app.get("/battle_action", response_class=JSONResponse)
async def battle_action(request: Request, action: str = Query(...)):

    result, updated_data = battle(game_state["monster_data"], game_state["player_data"], action)
    game_state["monster_data"], game_state["player_data"] = updated_data
    
    # プレイヤーが倒れた場合の処理
    if game_state["player_data"] is None:
        return {
            "result": result,
            "monster": None,
            "player": None,
            "game_clear": False,
            "game_over": True  # ゲームオーバーフラグを追加
        }
    
    # 新しいモンスターを生成
    if game_state["monster_data"] is None and game_state["player_data"]:
        game_state["monster_data"], game_state["player_data"] = monsterbox(game_state["player_data"])
        if game_state["monster_data"] is None:
            # 全てのモンスターを倒した場合
            return {"result": "ゲームクリア！ おめでとうございます！", "monster": None, "player": None, "game_clear": True}

        # 新しいモンスターが出現した場合の画像と名前とHP
        new_monster_image = get_monster_image_path(game_state["monster_data"][0])
        new_monster_name = game_state["monster_data"][0]
        new_monster_hp = game_state["monster_data"][1]
    else:
        new_monster_image = None
        new_monster_name = None
        new_monster_hp = None

    # モンスターが倒された場合、HPを None として返す
    monster_data = {
        "name": game_state["monster_data"][0] if game_state["monster_data"] else None,
        "hp": game_state["monster_data"][1] if game_state["monster_data"] else None
    }
    player_data = {
        "hp": game_state["player_data"][2],
        "mp": game_state["player_data"][4],
        "level": game_state["player_data"][1]
    }

    return {
        "result": result,
        "monster": monster_data,
        "player": player_data,
        "monster_image": f"/monster_images/{new_monster_image}" if new_monster_image else None,
        "monster_name": new_monster_name,
        "monster_hp": new_monster_hp,
        "game_clear": False,
        "game_over": False
    }

@app.get("/end", response_class=HTMLResponse)
async def end(request: Request):
    return templates.TemplateResponse("end.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
