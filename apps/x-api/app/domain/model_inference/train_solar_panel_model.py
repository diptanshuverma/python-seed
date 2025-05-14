# scripts/train_solar_status_model.py
import duckdb
import pandas as pd
import joblib
from pathlib import Path
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# Paths configuration
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "solar_panel_data"
INFO_FILE = DATA_DIR / "solar_panel_information.parquet"
LOC_FILE = DATA_DIR / "solar_panel_location.parquet"
TARGET_FILE = DATA_DIR / "solar_panel_data.parquet"
MODEL_DIR = BASE_DIR / "models"
MODEL_PATH = MODEL_DIR / "solar_status_model.pkl"

# Ensure model directory exists
MODEL_DIR.mkdir(parents=True, exist_ok=True)

# 1. Join Parquet sources via DuckDB
con = duckdb.connect()
join_query = f"""
CREATE OR REPLACE TABLE solar_panel_data AS
SELECT info.id,
       info.voltage,
       info.temperature,
       info.status,
       info.installation_timestamp,
       loc.latitude,
       loc.longitude
FROM read_parquet('{INFO_FILE}') AS info
JOIN read_parquet('{LOC_FILE}') AS loc
USING (id);
"""
con.execute(join_query)
# Export joined data
con.execute(f"COPY solar_panel_data TO '{TARGET_FILE}' (FORMAT PARQUET)")
print(f"Joined data written to {TARGET_FILE}")

# 2. Load joined data into pandas
df = pd.read_parquet(TARGET_FILE)

# 3. Feature engineering: convert timestamp to panel_age_days
# assuming installation_timestamp is in milliseconds
df['installation_timestamp'] = pd.to_datetime(df['installation_timestamp'], unit='ms')
current_time = pd.Timestamp.now()
df['panel_age_days'] = (current_time - df['installation_timestamp']).dt.days

# 4. Define feature matrix X and target y
feature_cols = ['voltage', 'temperature', 'latitude', 'longitude', 'panel_age_days']
X = df[feature_cols]
y = df['status']

# 5. Encode target labels
label_encoder = LabelEncoder()
y_enc = label_encoder.fit_transform(y)

# 6. Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y_enc, test_size=0.2, random_state=42, stratify=y_enc
)

# 7. Build ML pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

# 8. Train model
pipeline.fit(X_train, y_train)

# 9. Evaluate (optional)
train_score = pipeline.score(X_train, y_train)
test_score = pipeline.score(X_test, y_test)
print(f"Training accuracy: {train_score:.4f}")
print(f"Test accuracy: {test_score:.4f}")

# 10. Serialize pipeline + encoder
joblib.dump({'pipeline': pipeline, 'label_encoder': label_encoder}, MODEL_PATH)
print(f"Model & encoder saved to {MODEL_PATH}")
