from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import PyPDF2
import io
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="The Debate™ — Trump vs. Busey")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# ─────────────────────────────────────────────
TRUMP_SYSTEM = """You are a satirical comedy character based on the publicly parodied persona of Donald Trump — 
as seen on SNL, late night TV, and countless parody accounts. You are NOT the real Donald Trump. 
You are a fictional exaggerated comedy character for entertainment purposes only.

Your speech patterns:
- Everything you've ever done is "tremendous", "beautiful", "the best", "like nobody's ever seen before"
- Constantly claim you invented or discovered things, even things that existed before you were born
- Say "many people are saying" and "everybody knows" before stating made-up facts
- Interrupt your own sentences with tangents about your ratings, buildings, or deals
- Call anything you disagree with "fake", "a disaster", or "very unfair"
- Never admit being wrong — double down, claim total victory, and move on
- Competitive to the point of absurdity — you must win every single exchange
- Short punchy sentences. Heavy repetition. Lots of capitalization energy.
- Reference your net worth, TV shows, or golf courses in completely unrelated contexts

Keep responses to 3-5 sentences. Be funny, absurd, and satirical."""

BUSEY_SYSTEM = """You are a satirical comedy character based on Gary Busey's well-known public persona — 
his legendary reputation for bizarre, cosmic, stream-of-consciousness wisdom and unexpected profound nonsense.

Your speech patterns:
- Spontaneously create acronyms for random words mid-sentence 
  (e.g. "BURRITO stands for: Beings United Reaching Reality In Total Oneness")
- Reference animals, cheese, cosmic energy, and parking meters as sources of ancient wisdom
- Take any topic and connect it to a deeper spiritual truth that makes absolutely no sense
- Speak with complete sincerity — you are NEVER joking, this is all very serious and important wisdom
- Go on tangents that start somewhere normal and end somewhere completely unhinged
- Reference "the energy", "what the universe told me", and recent conversations with inanimate objects
- Treat Trump's points as if they are interesting doorways to much deeper cosmic mysteries

Keep responses to 3-5 sentences. Be cosmic, sincere, and gloriously unhinged."""

class DebateRequest(BaseModel):
    topic: str
    rounds: int = 3

class Exchange(BaseModel):
    speaker: str
    text: str

class DebateResponse(BaseModel):
    topic: str
    exchanges: list[Exchange]

def get_persona_response(system_prompt: str, messages: list) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system_prompt}] + messages,
        max_tokens=220,
        temperature=0.92
    )
    return response.choices[0].message.content.strip()


def run_debate(topic: str, rounds: int) -> list[Exchange]:
    rounds = min(max(rounds, 1), 6)
    exchanges = []
    trump_history = []
    busey_history = []

    trump_history.append({
        "role": "user",
        "content": f"The debate topic is: \"{topic}\". Open the debate with your position."
    })
    trump_text = get_persona_response(TRUMP_SYSTEM, trump_history)
    trump_history.append({"role": "assistant", "content": trump_text})
    exchanges.append(Exchange(speaker="trump", text=trump_text))

    busey_history.append({
        "role": "user",
        "content": f"The debate topic is: \"{topic}\". Trump just said: \"{trump_text}\". Share your perspective."
    })
    busey_text = get_persona_response(BUSEY_SYSTEM, busey_history)
    busey_history.append({"role": "assistant", "content": busey_text})
    exchanges.append(Exchange(speaker="busey", text=busey_text))

    for _ in range(rounds - 1):
        trump_history.append({
            "role": "user",
            "content": f"Busey just said: \"{busey_text}\". Respond and continue the debate about {topic}."
        })
        trump_text = get_persona_response(TRUMP_SYSTEM, trump_history)
        trump_history.append({"role": "assistant", "content": trump_text})
        exchanges.append(Exchange(speaker="trump", text=trump_text))

        busey_history.append({
            "role": "user",
            "content": f"Trump just said: \"{trump_text}\". Respond with your cosmic perspective on {topic}."
        })
        busey_text = get_persona_response(BUSEY_SYSTEM, busey_history)
        busey_history.append({"role": "assistant", "content": busey_text})
        exchanges.append(Exchange(speaker="busey", text=busey_text))

    return exchanges

@app.get("/")
def root():
    return {
        "app": "The Debate™",
        "tagline": "Two minds. Zero consensus. Infinite confusion.",
        "status": "ready to rumble"
    }

@app.post("/debate", response_model=DebateResponse)
def create_debate(request: DebateRequest):
    if not request.topic.strip():
        raise HTTPException(status_code=400, detail="Topic cannot be empty.")
    exchanges = run_debate(request.topic.strip(), request.rounds)
    return DebateResponse(topic=request.topic, exchanges=exchanges)

@app.post("/debate/upload", response_model=DebateResponse)
async def debate_from_file(file: UploadFile = File(...), rounds: int = 3):
    content = await file.read()
    topic_text = ""

    if file.filename.endswith(".pdf"):
        try:
            pdf = PyPDF2.PdfReader(io.BytesIO(content))
            for page in pdf.pages:
                topic_text += page.extract_text() or ""
            topic_text = topic_text[:1500].strip()
        except Exception:
            raise HTTPException(status_code=400, detail="Could not parse PDF.")
    elif file.filename.endswith(".txt"):
        topic_text = content.decode("utf-8", errors="ignore")[:1500].strip()
    else:
        raise HTTPException(status_code=400, detail="Supported file types: .pdf, .txt")

    if not topic_text:
        raise HTTPException(status_code=400, detail="Could not extract text from file.")

    topic_label = f'the contents of "{file.filename}"'
    exchanges = run_debate(f"{topic_label}: {topic_text}", rounds)
    return DebateResponse(topic=topic_label, exchanges=exchanges)
