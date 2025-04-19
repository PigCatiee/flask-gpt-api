from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime, timezone

# # 建立資料庫與資料表，只需要執行一次
# conn = sqlite3.connect('dialogues.db')
# c = conn.cursor()
# c.execute('''
#     CREATE TABLE IF NOT EXISTS dialogues (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         session_id TEXT,
#         prompt_text TEXT,
#         user_response TEXT,
#         timestamp TEXT
#     )
# ''')
# conn.commit()
# conn.close()

# print("✅ 資料庫已建立成功！")

###創建app
app = Flask(__name__)

@app.route('/clear_dialogues', methods=['POST'])
def clear_dialogues():
    try:
        conn = sqlite3.connect('dialogues.db')
        c = conn.cursor()
        c.execute('DELETE FROM dialogues')
        conn.commit()
        conn.close()
        print("🗑️ 所有資料已清空")
        return jsonify({"status": "cleared"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "🟢 Flask 正常運作中！"

@app.route('/save_dialogue', methods=['POST'])
def save_dialogue():
    data = request.get_json()
    prompt_text = data.get("prompt_text")
    user_response = data.get("user_response")
    session_id = data.get("session_id")

    # 取得 API 接收到的當地時間（台灣）
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    # 確認資料有被接收到
    print("✅ 收到資料：")
    print(f"Session_id: {session_id}")
    print(f"Prompt: {prompt_text}")
    print(f"Response: {user_response}")
    print(f"Timestamp: {timestamp}")

    # ⬇️ 寫入 SQLite 資料庫
    conn = sqlite3.connect("dialogues.db")
    c = conn.cursor()
    c.execute('''
        INSERT INTO dialogues (session_id, prompt_text, user_response, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (session_id, prompt_text, user_response, timestamp))
    conn.commit()
    conn.close()
    print("📝 資料儲存成功！") 

    return jsonify({"status": "received"}), 200

@app.route('/list_dialogues', methods=['GET'])
def list_dialogues():
    conn = sqlite3.connect('dialogues.db')
    c = conn.cursor()
    c.execute('SELECT * FROM dialogues')
    rows = c.fetchall()
    conn.close()

    # 把查詢結果轉成 JSON 格式
    results = [
        {"id": row[0], "session_id": row[1], "prompt_text": row[2], "user_response": row[3], "timestamp": row[4]}
        for row in rows
    ]

    return jsonify(results)


app.run(host='0.0.0.0', port=3000)
