import os
import pytz

from datetime import datetime
from supabase import create_client
from dotenv import load_dotenv
from fasthtml.common import *

# Load ENVs
load_dotenv()

MAX_NAME_CHAR = 30
MAX_MESSAGE_CHAR = 200
TIMESTAMP_FMT = "%Y-%m-%d %I:%M:%S %p UTC"

supabase = create_client(os.getenv("SUPABASE_PROJECT_URL"), os.getenv("SUPABASE_API_KEY"))

app, rt = fast_app(
    hdrs=(Link(rel="icon", type="assets/x-icon", href="/assets/bible.png"),),
)

def get_utc_time():
    utc_tz = pytz.timezone("UTC")
    return datetime.now(utc_tz)

def add_message(name, message):
    timestamp = get_utc_time().strftime(TIMESTAMP_FMT)
    supabase.table("OpenScroll").insert(
        {"name": name, "message": message, "timestamp": timestamp}
    ).execute()

def get_messages():
    response = (
        supabase.table("OpenScroll").select("*").order("id", desc=True).execute()
    )
    return response.data

@rt('/')
def get():
    return Titled("OpenScroll 📜 ", render_content())

def render_message(entry):
    return Article(
            Header(f"Name: {entry['name']}"),
            P(entry["message"]),
            Footer(Small(Em(f"Posted: {entry['timestamp']}"))),
        ),

def render_message_list():
    messages = get_messages()

    return Div(
        *[render_message(entry) for entry in messages],
        id="message-list"
    )

def render_content():
    form = Form(
        Fieldset(
            Input(
                type="text",
                name="name",
                placeholder="Name",
                required=True,
                maxlength=MAX_NAME_CHAR,
            ),
            Input(
                type="text",
                name="message",
                placeholder="Message",
                required=True,
                maxlength=MAX_MESSAGE_CHAR,
            ),
            Button("Submit", type="submit"),
        ),
        method="post",
        hx_post="/submit-message",
        hx_target="#message-list", #only swap the message list
        hx_swap="outerHTML",
        hx_on__after_request="this.rest()", #rests the form after submission

    )

    intro = Div( P("")
                 ,H3("Welcome to OpenScroll"),
                 I("A quiet space to share the scriptures that speak to your heart."),
                 P(""),
                 P("Whether it’s a verse that lifted you in hard times, inspired your faith, or simply stayed with you, we invite you to share it here. Browse what others have written, reflect on God’s Word, and add your own favorite scripture to the scroll.")
                 )

    return Div(
        intro,
        P(Em("Share your scripture here!")),
        form,
        Div(
            "Made with FastHTML by ",
            A("Prov", href="https://github.com/directlypro", target="_blank"),
        ),
        Hr(),
        render_message_list(),
    )

@rt("/submit-message", methods=["POST"])
def post(name: str, message: str):
    add_message(name, message)
    return render_message_list()

serve()