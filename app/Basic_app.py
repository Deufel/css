# /// script
# dependencies = ["apsw", "html_tags", "py_sse"]
# ///

import secrets
from html_tags import pretty, Html, Head, Body, Datastar, ScopedCSS, Favicon, Header, Nav, Main, Aside, Footer, H1, H2, H3, Div, Span, Button, P, A, Section, Article, Em, Small, Strong, Kbd, Code, Pre, Hr, Input, Meta, Title, Script, Style
from py_sse import serve, create_app, create_relay, create_signer, patch_elements, patch_signals, signals, set_cookie
import os
import apsw
import apsw.bestpractice

app = create_app()
relay = create_relay()
PASSCODE = '0000'
NAMES = ['Fox', 'Owl', 'Bear', 'Wolf', 'Hawk']
db_sql = "\n    CREATE TABLE IF NOT EXISTS users (\n        user_id    INTEGER PRIMARY KEY AUTOINCREMENT,\n        user_name  TEXT NOT NULL,\n        created_at REAL DEFAULT (julianday('now'))\n    );\n\n    CREATE TABLE IF NOT EXISTS messages (\n        msg_id     INTEGER PRIMARY KEY AUTOINCREMENT,\n        user_id    INTEGER REFERENCES users(user_id),\n        message    TEXT NOT NULL,\n        created_at REAL DEFAULT (julianday('now'))\n    );\n\n    CREATE TABLE IF NOT EXISTS evt (\n        evt_id  INTEGER PRIMARY KEY AUTOINCREMENT,\n        ts      REAL    DEFAULT (julianday('now')),\n        cmd     TEXT,\n        user_id INTEGER REFERENCES users(user_id),\n        payload TEXT\n    );\n    "
db = apsw.Connection(':memmory')

apsw.bestpractice.apply(apsw.bestpractice.recommended)
db.execute(db_sql)

def render_messages():
    return Div(*[Div(Span(m["user"], style="font-weight:bold"), " ", Span(m["message"])) for m in load_msgs()], id="messages")

@app.get("/")
async def home(req):
    suggestion = secrets.choice(NAMES) + str(secrets.randbelow(100))
    return Html(
        Head(Title("Chat"), Datastar(), ScopedCSS(), Favicon("🔥")),
        Body(
            H2("Enter Chat"),
            Input(id="username", placeholder="Username", value="whatever", data_bind="userName"),
            Input(id="password", placeholder="passcode", value="",          data_bind="passcode"),
            Button({"data-on:click": "@post('/login')"}, "Enter")
            )
        )

@app.post("/login")
async def login(req):
    data = await signals(req)
    username = data.get("userName", "").strip()
    passcode = data.get("passcode", "").strip()
    if not username or passcode != PASSCODE: return ("/", 302)
    get_or_create_user(username)
    set_cookie(req, "user", username, path="/", http_only=True)
    return ("/chat", 302)

@app.get("/chat")
async def chat(req):
    user = req["cookies"].get("user")
    if not user:
        return ("/", 302)
    return Html(
       Head(Title("Chat"), Datastar(), ScopedCSS(), Favicon("🔥")),
        Body(
            Header(H2("Mini Chat"), P(f"You are: {user}")),
            Main(Div(id="messages", **{"data-init": "@get('/stream')"})),
            Footer(
                Input(data_bind="text", placeholder="Type a message..."),
                Button({"data-on:click": "@post('/send')"}, "Send"))))

@app.post("/send")
async def send(req):
    data = await signals(req)
    text = data.get("text", "").strip()
    user = req["cookies"].get("user")
    if not text or not user: return None
    user_id = get_or_create_user(user)
    save_msg(user_id, text)
    relay.publish("chat.message", user)
    return None

@app.get("/stream")
async def stream(req):
    user = req["cookies"].get("user")
    if not user:
        return

    # Send current messages immediately on connect
    yield patch_elements(render_messages())

    # Then wait for new events and re-render
    async for topic, data in relay.subscribe("chat.*"):
        yield patch_elements(render_messages())

def conn(): return apsw.Connection("chat.db")

def get_or_create_user(name):
    r = list(db.execute("SELECT user_id FROM users WHERE user_name=?", (name,)))
    if r: return r[0][0]
    db.execute("INSERT INTO users(user_name) VALUES(?)", (name,))
    return db.last_insert_rowid()

def save_msg(user_id, message):
    db.execute("INSERT INTO messages(user_id, message) VALUES(?,?)", (user_id, message))

def load_msgs():
    sql = """SELECT u.user_name, m.message, m.created_at
             FROM messages m JOIN users u USING(user_id)
             ORDER BY m.created_at"""
    return [dict(user=r[0], message=r[1], ts=r[2]) for r in db.execute(sql)]


serve(app)
