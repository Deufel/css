import marimo

__generated_with = "0.22.0"
app = marimo.App(width="medium")

with app.setup:
    import secrets

    from html_tags import pretty, Html, Head, Body, Datastar, ScopedCSS, Favicon, Header, Nav, Main, Aside, Footer, H1, H2, H3, Div, Span, Button, P, A, Section, Article, Em, Small, Strong, Kbd, Code, Pre, Hr, Input, Meta, Title, Script, Style

    from py_sse import serve, create_app, create_relay, create_signer, patch_elements, patch_signals, signals, set_cookie

    import os
    import apsw
    import apsw.bestpractice

    app = create_app()
    relay = create_relay()

    PASSCODE = "0000"
    NAMES = ["Fox", "Owl", "Bear", "Wolf", "Hawk"]



    db_sql = '''
    CREATE TABLE IF NOT EXISTS users (
        user_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name  TEXT NOT NULL,
        created_at REAL DEFAULT (julianday('now'))
    );

    CREATE TABLE IF NOT EXISTS messages (
        msg_id     INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id    INTEGER REFERENCES users(user_id),
        message    TEXT NOT NULL,
        created_at REAL DEFAULT (julianday('now'))
    );

    CREATE TABLE IF NOT EXISTS evt (
        evt_id  INTEGER PRIMARY KEY AUTOINCREMENT,
        ts      REAL    DEFAULT (julianday('now')),
        cmd     TEXT,
        user_id INTEGER REFERENCES users(user_id),
        payload TEXT
    );
    '''

            
    apsw.bestpractice.apply(apsw.bestpractice.recommended)

    # os.unlink("chat.db")
    #db = apsw.Connection(:memmory:)
    #db.execute(db_sql)

    db = apsw.Connection(":memmory")
    db.execute(db_sql) 


@app.cell
def _():
    from py_sse.mserver import serve_background, ServerState, stop_background


    import ngrok

    return


@app.function
def render_event_log():
    evts = load_events()
    return Aside(
        H3("Event Log"),
        *[Div(
            Small(e["time"]),
            " ",
            Kbd(e["cmd"]),
            " ",
            Span(e["user"]),
            " ",
            Button({"data-on:click": f"@post('/rewind?to={e['id']}')"}, "↩"),
            style="margin-bottom:0.25rem"
        ) for e in evts],
        id="eventlog"
    )


@app.function
def render_messages(msgs=None):
    if msgs is None:
        msgs = load_msgs()
    return Div(
        *[Div(Span(m["user"], style="font-weight:bold"), " ", Span(m["message"]))
          for m in msgs],
        id="messages"
    )


@app.function
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


@app.function
@app.post("/login")
async def login(req):
    data = await signals(req)
    username = data.get("userName", "").strip()
    passcode = data.get("passcode", "").strip()
    if not username or passcode != PASSCODE: return ("/", 302)
    get_or_create_user(username)
    set_cookie(req, "user", username, path="/", http_only=True)
    return ("/chat", 302)


@app.function
@app.get("/chat")
async def chat(req):
    user = req["cookies"].get("user")
    if not user:
        return ("/", 302)
    return Html(
        Head(Title("Chat"), Datastar(), ScopedCSS(), Favicon("🔥")),
        Body(
            Header(H2("Mini Chat"), P(f"You are: {user}")),
            Div(
                Main(Div(id="messages", **{"data-init": "@get('/stream')"})),
                Aside(Div(id="eventlog", **{"data-init": "@get('/evtstream')"})),
                style="display:flex; gap:1rem"
            ),
            Footer(
                Input(data_bind="text", placeholder="Type a message..."),
                Button({"data-on:click": "@post('/send')"}, "Send"))))


@app.function
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


@app.function
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


@app.cell
def _():
    # state  = serve_background(app, port=8000)
    #input("any key to stop server")
    return


@app.cell
def _():
    # stop_background(state)
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Database
    """)
    return


@app.function
def conn(): return apsw.Connection("chat.db")


@app.cell
def _():
    return


@app.function
def load_msgs():
    sql = """SELECT u.user_name, m.message, m.created_at
             FROM messages m JOIN users u USING(user_id)
             ORDER BY m.created_at"""
    return [dict(user=r[0], message=r[1], ts=r[2]) for r in db.execute(sql)]


@app.function
def log_evt(cmd, user_id, payload=""):
    db.execute("INSERT INTO evt(cmd, user_id, payload) VALUES(?,?,?)", (cmd, user_id, payload))


@app.function
def get_or_create_user(name):
    r = list(db.execute("SELECT user_id FROM users WHERE user_name=?", (name,)))
    if r:
        return r[0][0]
    db.execute("INSERT INTO users(user_name) VALUES(?)", (name,))
    uid = db.last_insert_rowid()
    log_evt("user.create", uid, name)
    return uid


@app.function
def save_msg(user_id, message):
    db.execute("INSERT INTO messages(user_id, message) VALUES(?,?)", (user_id, message))
    log_evt("msg.send", user_id, message)


@app.function
def load_events():
    sql = """SELECT evt_id, cmd, u.user_name, e.payload,
                    strftime('%H:%M:%S', e.ts) as time
             FROM evt e JOIN users u USING(user_id)
             ORDER BY e.evt_id"""
    return [dict(id=r[0], cmd=r[1], user=r[2], payload=r[3], time=r[4])
            for r in db.execute(sql)]


@app.function
def load_msgs_until(evt_id):
    """Replay messages using only events up to evt_id"""
    sql = """SELECT u.user_name, e.payload
             FROM evt e JOIN users u USING(user_id)
             WHERE e.cmd = 'msg.send' AND e.evt_id <= ?
             ORDER BY e.evt_id"""
    return [dict(user=r[0], message=r[1]) for r in db.execute(sql, (evt_id,))]


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Rewind
    """)
    return


@app.function
@app.post("/rewind")
async def rewind(req):
    evt_id = int(req.get("query", {}).get("to", 0))
    if not evt_id:
        return None
    msgs = load_msgs_until(evt_id)
    relay.publish("chat.rewind", str(evt_id))
    return patch_elements(render_messages(msgs))


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Event Stream log
    """)
    return


@app.function
@app.get("/evtstream")
async def evtstream(req):
    yield patch_elements(render_event_log())
    async for topic, data in relay.subscribe("chat.*"):
        yield patch_elements(render_event_log())


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
