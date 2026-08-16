# Jobify

AI-powered job fit analyzer that evaluates a candidate's **resume**, **self-description**, and **job description** to generate an evidence-based match analysis.

## Tech Stack

* Python
* FastAPI
* Pydantic
* Beanie(ODM)
* Google Gemini
* uv
* pypdf

## Setup

```bash
git clone https://github.com/Abhishekkrsingh2023/Jobify.git
cd Jobify

uv sync
```

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key
MONGO_URI=mongodb://user_name:password@localhost:27017/
MONGO_DATABASE=jobify
```

Run the server:

```bash
uv run uvicorn app.main:app --reload
```

API docs:

```text
http://localhost:8000/docs
```

## API

### `POST /upload`

Accepts:

* `resume` — PDF resume
* `self_description` — candidate description
* `job_description` — target job description

Returns a structured analysis containing:

* Match percentage
* Skill status (`matched`, `partial`, `missing`)
* Evidence
* Strengths
* Skill gaps
* Readiness
* Summary

## License

MIT
