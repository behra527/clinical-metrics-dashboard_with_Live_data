# Clinical Metrics Dashboard

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.64.0-red?logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-3.0.5-150458?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-7.1.0-3F4F75?logo=plotly)

An interactive clinical dashboard built with **Python, Streamlit, Pandas, and Plotly** for monitoring patient metrics, vital-sign trends, and readmission risk.

## Features

* Patient selection with dynamic profile and metrics
* Blood pressure and glucose monitoring
* Interactive vital-sign trend charts
* Adjustable readmission-risk threshold
* Date-range filtering
* Risk distribution and risk gauge
* Dynamic tables and CSV export
* Streamlit session state for interactive values

## Tech Stack

* Python
* Streamlit
* Pandas
* Plotly
* NumPy

## Project Structure

```text
clinical-metrics-dashboard/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   ├── data_generator.py
│   ├── patients.csv
│   └── vitals.csv
└── src/
    ├── charts.py
    ├── data_loader.py
    └── metrics.py
```

## Run Locally

```bash
git clone https://github.com/YOUR_USERNAME/clinical-metrics-dashboard.git
cd clinical-metrics-dashboard
pip install -r requirements.txt
python -m streamlit run app.py
```

## Dataset

The dashboard uses synthetic clinical data containing **50 patients and 300 vital records**.

## Disclaimer

This project uses synthetic data for demonstration and development purposes only. It is not intended for clinical diagnosis, treatment, or medical decision-making.
