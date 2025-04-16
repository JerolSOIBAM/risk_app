# Trade Risk Calculator

A Streamlit web application for calculating optimal position sizes and managing risk in trading.

## Features

- Standard Risk Calculator for basic risk assessment
- Position Size Calculator for fine-tuning based on technical analysis
- Risk-to-Reward ratio calculations
- 3-part exit strategy recommendations
- Dark theme UI for better visibility

## Installation

1. Clone this repository:
```bash
git clone <your-repository-url>
cd streamlit_risk_app
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Running the App Locally

To run the app locally, use the following command:
```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## Deployment

The app can be deployed on Streamlit Cloud:

1. Create a GitHub repository and push your code
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Click "New app" and connect your GitHub repository
4. Select the main file (app.py) and branch
5. Click "Deploy"

## Usage

1. **Standard Risk Calculator**:
   - Enter your account size
   - Set your risk percentage
   - Input number of shares and entry price
   - Set your target price

2. **Position Size Calculator**:
   - Enter your account size
   - Set your risk percentage
   - Input entry price and technical stop loss
   - Set your target price

The app will calculate:
- Optimal position sizes
- Risk-to-reward ratios
- Stop loss levels
- Capital requirements

