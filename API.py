# Import FastAPI for building the web server
# Import pandas for reading/manipulating the dataset
from fastapi import FastAPI
import pandas as pd
from pathlib import Path  # safer path handling across OSes

# -----------------------------
# Step 1: Create the FastAPI app
# -----------------------------
app = FastAPI(
    title="Stress Dataset API",           # Metadata: visible in auto docs
    description="A simple API to serve the stress dataset",
    version="1.0.0"
)

# -----------------------------
# Step 2: Define dataset path
# -----------------------------
# BASE_DIR = folder where this script lives
BASE_DIR = Path(__file__).resolve().parent

# DATA_PATH = data/stress_dataset.csv inside the repo
DATA_PATH = BASE_DIR / "data" / "stress_dataset.csv"

# -----------------------------
# Step 3: Load dataset once at startup
# -----------------------------
try:
    df = pd.read_csv(DATA_PATH)  # read CSV into a DataFrame
except FileNotFoundError:
    # Give a clear error if the file isn't found
    raise RuntimeError(f"Dataset not found at {DATA_PATH}. Make sure it exists.")

# -----------------------------
# Step 4: Define the stress column name
# -----------------------------
STRESS_COL = "Which type of stress do you primarily experience?"

# -----------------------------
# Step 5: Health check endpoint
# -----------------------------
@app.get("/health")  # GET request to /health
def health_check():
    """
    Returns a simple OK status to check if the server is running.
    """
    return {"status": "ok"}  # JSON response

# -----------------------------
# Step 6: Full dataset endpoint
# -----------------------------
@app.get("/data/full")  # GET request to /data/full
def get_full_data():
    """
    Returns the entire dataset as a JSON list of records.
    """
    # df.to_dict(orient="records") converts DataFrame to a list of dicts
    # Example: [{"age": 22, "stress": "high"}, {...}, ...]
    return df.to_dict(orient="records")

# -----------------------------
# Step 7: Stress-only endpoint
# -----------------------------
@app.get("/data/stress")  # GET request to /data/stress
def get_stress_data():
    """
    Returns only ID and stress column.
    """
    # Make sure the column exists
    if STRESS_COL not in df.columns:
        return {"error": f"Column '{STRESS_COL}' not found in dataset."}

    # Select only the stress column and reset index for IDs
    stress_df = df[[STRESS_COL]].reset_index(drop=True)

    # Create an 'id' column starting from 1
    stress_df.insert(0, "id", stress_df.index + 1)

    # Convert to JSON list of records
    return stress_df.to_dict(orient="records")
