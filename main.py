import os
import pytz

from datetime import datetime
from supabase import create_client
from dotenv import load_dotenv
from fasthtml.common import *

# Load ENVs
load_dotenv()

MAX_NAME_CHAR = 110
MAX_MESSAGE_CHAR = 1200
TIMESTAMP_FMT = "%Y-%m-%d %I:%M:%S %p UTC"

supabase = create_client(os.getenv("SUPABASE_PROJECT_URL"), os.getenv("SUPABASE_API_KEY"))

# Enhanced CSS with biblical theming and modern design
biblical_css = Style("""
    @import url('https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=Playfair+Display:wght@400;700&display=swap');

    :root {
        --parchment: #f9f6f0;
        --deep-gold: #d4af37;
        --rich-brown: #8b4513;
        --dark-brown: #654321;
        --soft-cream: #fef8f0;
        --shadow-brown: rgba(139, 69, 19, 0.1);
        --accent-red: #8b0000;
        --text-dark: #2c1810;
        --scroll-gradient: linear-gradient(135deg, #f9f6f0 0%, #f0e6d2 100%);
    }

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body {
        font-family: 'Crimson Text', serif;
        background: var(--scroll-gradient);
        color: var(--text-dark);
        line-height: 1.7;
        min-height: 100vh;
        background-attachment: fixed;
    }

    /* Decorative scroll container */
    .scroll-container {
        max-width: 800px;
        margin: 0 auto;
        background: var(--parchment);
        box-shadow: 0 20px 60px rgba(139, 69, 19, 0.3);
        position: relative;
        border-radius: 15px;
        overflow: hidden;
    }

    /* Decorative scroll edges */
    .scroll-container::before,
    .scroll-container::after {
        content: '';
        position: absolute;
        left: 0;
        right: 0;
        height: 20px;
        background: linear-gradient(90deg,
            var(--rich-brown) 0%,
            var(--deep-gold) 15%,
            var(--parchment) 25%,
            var(--parchment) 75%,
            var(--deep-gold) 85%,
            var(--rich-brown) 100%);
        z-index: 10;
    }

    .scroll-container::before {
        top: 0;
        border-radius: 15px 15px 0 0;
    }

    .scroll-container::after {
        bottom: 0;
        border-radius: 0 0 15px 15px;
    }

    /* Main content padding */
    .main-content {
        padding: 40px 50px;
        position: relative;
        z-index: 5;
    }

    /* Header styling */
    h1 {
        font-family: 'Playfair Display', serif;
        font-size: 3rem;
        color: var(--rich-brown);
        text-align: center;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(139, 69, 19, 0.2);
        position: relative;
    }

    h1::after {
        content: '📜';
        display: block;
        font-size: 2rem;
        margin-top: 10px;
        opacity: 0.7;
    }

    h3 {
        font-family: 'Playfair Display', serif;
        color: var(--dark-brown);
        font-size: 1.8rem;
        margin-bottom: 15px;
        text-align: center;
    }

    /* Introduction section */
    .intro-section {
        text-align: center;
        margin-bottom: 40px;
        padding: 30px;
        background: rgba(255, 255, 255, 0.4);
        border-radius: 10px;
        border: 2px solid var(--deep-gold);
        position: relative;
    }

    .intro-section::before {
        content: '"';
        position: absolute;
        top: -10px;
        left: 20px;
        font-size: 4rem;
        color: var(--deep-gold);
        font-family: 'Playfair Display', serif;
    }

    .intro-section p {
        font-size: 1.2rem;
        color: black;
        margin-bottom: 15px;
        font-style: italic;
    }

    /* Form styling */
    .scripture-form {
        background: rgba(255, 255, 255, 0.6);
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 30px;
        border: 3px solid var(--deep-gold);
        box-shadow: 0 10px 30px var(--shadow-brown);
        position: relative;
    }

    .form-title {
        text-align: center;
        color: var(--dark-brown);
        font-size: 1.3rem;
        margin-bottom: 25px;
        font-style: italic;
    }

    fieldset {
        border: none;
        display: flex;
        flex-direction: column;
        gap: 20px;
    }

    input[type="text"] {
        padding: 15px 20px;
        border: 2px solid var(--deep-gold);
        border-radius: 8px;
        font-family: 'Crimson Text', serif;
        font-size: 1.1rem;
        background: var(--soft-cream);
        color: var(--text-dark);
        transition: all 0.3s ease;
    }

    input[type="text"]:focus {
        outline: none;
        border-color: var(--rich-brown);
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.3);
        background: white;
        transform: translateY(-2px);
    }

    input[type="text"]::placeholder {
        color: var(--rich-brown);
        opacity: 0.7;
        font-style: italic;
    }

    button {
        padding: 15px 30px;
        background: linear-gradient(135deg, var(--deep-gold) 0%, var(--rich-brown) 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-family: 'Playfair Display', serif;
        font-size: 1.2rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 5px 15px rgba(139, 69, 19, 0.3);
    }

    button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(139, 69, 19, 0.4);
        background: linear-gradient(135deg, var(--rich-brown) 0%, var(--deep-gold) 100%);
    }

    /* Messages section */
    .messages-header {
        text-align: center;
        margin: 40px 0 30px;
        position: relative;
    }

    .messages-header::before,
    .messages-header::after {
        content: '';
        position: absolute;
        top: 50%;
        width: 100px;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--deep-gold), transparent);
    }

    .messages-header::before { left: 0; }
    .messages-header::after { right: 0; }

    .messages-header h3 {
        display: inline-block;
        # background: var(--parchment);
        padding: 0 20px;
        margin: 0;
    }

    /* Individual message styling */
    div#message-list > div {
        background: rgba(255, 255, 255, 0.8);
        margin-bottom: 25px;
        padding: 25px;
        border-radius: 12px;
        border-left: 5px solid var(--deep-gold);
        box-shadow: 0 5px 20px var(--shadow-brown);
        transition: all 0.3s ease;
        position: relative;
    }

    div#message-list > div:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(139, 69, 19, 0.2);
        background: rgba(255, 255, 255, 0.95);
    }

    div#message-list > div::before {
        content: '"';
        position: absolute;
        top: 10px;
        left: 10px;
        font-size: 2rem;
        color: var(--deep-gold);
        opacity: 0.3;
        font-family: 'Playfair Display', serif;
    }

    div#message-list > div > div:first-child {
        color: var(--rich-brown);
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 12px;
        font-family: 'Playfair Display', serif;
    }

    div#message-list > div p {
        font-size: 1.1rem;
        line-height: 1.8;
        margin-bottom: 15px;
        text-indent: 20px;
        color: var(--text-dark);
    }

    div#message-list > div > div:last-child {
        text-align: right;
        color: var(--rich-brown);
        font-style: italic;
        opacity: 0.8;
        font-size: 0.9rem;
    }

    /* Footer styling */
    .site-footer {
        text-align: center;
        font-size: 1.1rem;
        padding: 20px;
        border-top: 2px solid var(--deep-gold);
        margin-top: 30px;
        background: rgba(255, 255, 255, 0.3);
        font-style: italic;
    }

    .site-footer a {
        color: var(--rich-brown);
        text-decoration: none;
        font-weight: 600;
        transition: color 0.3s ease;
    }

    .site-footer a:hover {
        color: var(--deep-gold);
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .scroll-container {
            margin: 10px;
            border-radius: 10px;
        }

        .main-content {
            padding: 30px 25px;
        }

        h1 {
            font-size: 2.2rem;
        }

        .intro-section,
        .scripture-form {
            padding: 20px;
        }

        fieldset {
            gap: 15px;
        }

        input[type="text"] {
            padding: 12px 15px;
        }

        button {
            padding: 12px 25px;
        }

        article {
            padding: 20px;
        }
    }

    /* Subtle animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    article {
        animation: fadeInUp 0.6s ease-out;
    }

    /* Loading states */
    .htmx-request {
        opacity: 0.7;
        transition: opacity 0.3s ease;
    }

    .htmx-request button {
        position: relative;
        color: transparent;
    }

    .htmx-request button::after {
        content: 'Sharing...';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: white;
        font-size: 1rem;
    }
""")

app, rt = fast_app(
    hdrs=(
        Link(rel="icon", type="assets/x-icon", href="/assets/bible.png"),
        biblical_css,
    ),
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
    return Title("OpenScroll 📜"), render_content()


def render_message(entry):
    return Div(
        Div(f"Shared by {entry['name']}"),
        P(entry["message"]),
        Div(Small(Em(f"Written on {entry['timestamp']}"))),
    )


def render_message_list():
    messages = get_messages()

    if not messages:
        return Div(
            Div(
                P("No scriptures have been shared yet. Be the first to add a verse that speaks to your heart!",
                  style="text-align: center; font-style: italic; color: var(--rich-brown); padding: 40px;")
            ),
            id="message-list"
        )

    return Div(
        Div(
            H3("Shared Scriptures", style="margin-bottom: 0;"),
            cls="messages-header"
        ),
        *[render_message(entry) for entry in messages],
        id="message-list"
    )


def render_content():
    form = Form(
        P("Share your scripture here!", cls="form-title"),
        Fieldset(
            Input(
                type="text",
                name="name",
                placeholder="Your name (e.g., David, Sarah, etc.)",
                required=True,
                maxlength=MAX_NAME_CHAR,
            ),
            Input(
                type="text",
                name="message",
                placeholder="Enter your favorite scripture verse and why it speaks to you...",
                required=True,
                maxlength=MAX_MESSAGE_CHAR,
            ),
            Button("Share This Scripture", type="submit"),
        ),
        method="post",
        hx_post="/submit-message",
        hx_target="#message-list",
        hx_swap="outerHTML",
        hx_on__after_request="if(event.detail.xhr.status === 200) this.reset()",
        cls="scripture-form"
    )

    intro = Div(
        H3("Welcome to OpenScroll"),
        P("A sacred space to share the scriptures that speak to your heart."),
        P("Whether it's a verse that lifted you in hard times, inspired your faith, or simply stayed with you throughout your journey, we invite you to share it here."),
        P("Browse the wisdom others have shared, reflect on God's Word, and add your own treasured scripture to this digital scroll."),
        cls="intro-section"
    )

    return Div(
        Div(
            H1("OpenScroll"),
            intro,
            form,
            Div(
                "Crafted with love using FastHTML by ",
                A("Prov", href="https://github.com/directlypro", target="_blank"),
                " • A place for God's Word to dwell",
                cls="site-footer"
            ),
            render_message_list(),
            cls="main-content"
        ),
        cls="scroll-container"
    )


@rt("/submit-message", methods=["POST"])
def post(name: str, message: str):
    add_message(name, message)
    return render_message_list()


serve()