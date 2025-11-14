git init

pip install uv
uv venv
.venv\Scripts\activate
uv pip install fastapi uvicorn python-dotenv supabase
uv run uvicorn main:app --reload
