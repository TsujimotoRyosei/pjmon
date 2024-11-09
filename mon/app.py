from fastapi import FastAPI, Request, Form, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from danjon import playerpm,battle
import random
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="mon/templates")

player_data = {
    "username": None,
    "level": 1,
    "hp": 0,
    "mp": 0,
}

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("web.html", {"request": request, "player": player_data})

@app.post("/player_status")
async def player_status(request: Request, username: str = Form(...)):
    player_data["username"] = username
    player_data["level"] = 1
    player_data["hp"] = random.randint(50, 100)
    player_data["mp"] = random.randint(70, 100)
    return templates.TemplateResponse("web.html", {"request": request, "player": player_data})

@app.get("/start_game", response_class=HTMLResponse)
async def start_game(request: Request):
    # バトル画面に移行
    result = playerpm()  # モンスター出現の初期メッセージ
    return templates.TemplateResponse("battle.html", {"request": request, "player": player_data, "result": result})

@app.get("/battle_action")
async def battle_action(action: str = Query(...)):
    # 各アクションの結果を生成し返す（簡略化した例）
    if action == "attack":
        result = "プレイヤーが攻撃しました！ モンスターに 10 のダメージ！"
    elif action == "magic":
        result = "プレイヤーが魔法を使いました！ モンスターに 20 のダメージ！"
    elif action == "heal":
        result = "プレイヤーが回復しました！ HP が 15 回復！"
    elif action == "run":
        result = "プレイヤーは逃げ出したが、失敗した！"
    else:
        result = "不明な行動です。"
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
