# ☁️ CloudCost – Cloud Storage Cost Comparison Tool

CloudCost calculates and compares monthly cloud storage costs for **AWS S3**, **Google Cloud** and **Microsoft Azure**, and shows the cheapest provider.

## Features
- Enter required storage in GB or TB
- Compare provider pricing and monthly/yearly cost
- Highlights the cheapest provider
- Downloadable cost comparison report (.txt) and data (.csv)

## Tech
Python · Streamlit · VS Code · Git & GitHub

## Setup
```bash
git clone https://github.com/<your-username>/CloudCost.git
cd CloudCost
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Run tests
```bash
pytest -v
```

## Sample output (500 GB)
| Provider | Monthly Cost |
|---|---|
| AWS S3 | $11.50 |
| Google Cloud | $10.00 |
| Microsoft Azure | $9.50 |

Result: **Microsoft Azure** is the cheapest based on the example prices.

> Illustrative prices only, not live provider quotes. Edit `PRICING` in `calculator.py` to use current rates. 1 TB is treated as 1024 GB.

## Project structure
```
CloudCost/
├── app.py              # Streamlit UI
├── calculator.py       # Cost logic and report generation
├── test_calculator.py  # Unit tests
├── requirements.txt
├── README.md
├── LICENSE
└── screenshots/        # Add app screenshots here
```

## Screenshots
Add images to `screenshots/` and reference them here, e.g. `![App](screenshots/app.png)`.

## License
MIT
