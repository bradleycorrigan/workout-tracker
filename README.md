<!-- ...existing code... -->

# Python Streamlit Workout Tracker

A simple Streamlit app to log workouts and sync them to Supabase.

The app:
- lets you input workouts from a Streamlit UI,
- loads exercise options from a Supabase table,
- writes workout entries to a Supabase table,
- groups and orders workout history by day for easier review.

---

## Features

- **Exercise picker** populated from Supabase
- **Workout logging** (date + exercise details)
- **Supabase-backed storage** for persistent tracking
- **Grouped daily view** of workouts
- **Streamlit interface** for fast local usage

---

## Tech Stack

- **Python**
- **Streamlit**
- **Supabase (Postgres)**
- Optional: `pandas` for formatting/display

---

## Project Structure

```text
workout-tracker/
├── main.py          # Streamlit app entrypoint
├── README.md
└── requirements.txt # dependencies (if present)
```

---

## Setup

### 1) Clone and open

### 2) Create and activate a virtual environment (macOS)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

```bash
pip install streamlit supabase pandas python-dotenv
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_or_service_key
```

If `main.py` uses different names, match those exactly.

---

## Supabase Tables

This app expects:
1. an **exercises table** used to populate exercise options,
2. a **workouts table** used to store logged sessions.

Typical fields might include:

- `exercises`: `id`, `name`
- `workouts`: `id`, `workout_date`, `exercise`, `sets`, `reps`, `weight`, `notes`, `created_at`

Use the exact schema referenced in `main.py`.

---

## Run the App

```bash
streamlit run main.py
```

Then open the local URL shown in terminal (usually `http://localhost:8501`).

---

## How It Works

At a high level, `main.py`:
1. initializes a Supabase client from environment variables,
2. fetches exercise data for UI selection,
3. accepts workout input via Streamlit form controls,
4. inserts workout rows into Supabase,
5. queries saved workouts and displays them grouped/sorted by day.

---

## Troubleshooting

- **App won’t start**: verify your virtual environment and installed packages.
- **Supabase auth errors**: check `SUPABASE_URL` and `SUPABASE_KEY`.
- **No exercises shown**: confirm exercises table exists and has rows.
- **Insert fails**: ensure workout payload keys match table column names.

---

## Future Improvements

- Edit/delete logged workouts
- Charts for volume/progression over time
- Filters by date range, exercise, muscle group
- Authentication per user
- Export to CSV

---

## License

Add your preferred license here (e.g., MIT).