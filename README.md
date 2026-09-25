# Clinical Metrics Dashboard

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.64.0-FF4B4B?style=for-the-badge\&logo=streamlit\&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-3.0.5-150458?style=for-the-badge\&logo=pandas\&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-7.1.0-3F4F75?style=for-the-badge\&logo=plotly\&logoColor=white)

An interactive clinical dashboard built with **Python, Streamlit, Pandas, and Plotly** for monitoring patient metrics, vital-sign trends, readmission risk, and visit history.

## Features

* Patient selection with dynamic profile and metrics
* Date-range filtering
* Blood pressure and glucose monitoring
* Interactive vital-sign trend charts
* Adjustable readmission-risk threshold
* Risk distribution and risk gauge
* Dynamic visit history table
* CSV export
* Streamlit session state for interactive values

## Tech Stack

| Technology | Purpose                   |
| ---------- | ------------------------- |
| Python     | Application development   |
| Streamlit  | Dashboard and UI          |
| Pandas     | Data processing           |
| Plotly     | Interactive visualization |
| NumPy      | Synthetic data generation |

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
git clone https://github.com/behra527/clinical-metrics-dashboard_with_Live_data.git
cd clinical-metrics-dashboard_with_Live_data
pip install -r requirements.txt
python -m streamlit run app.py
```

## Dataset

The dashboard uses synthetic clinical data containing **50 patients and 300 vital records**.

The data includes:

* Patient demographics
* Clinical visits
* Blood pressure
* Glucose levels
* Readmission risk

## Disclaimer

This project uses synthetic data for demonstration and development purposes only. It is not intended for medical diagnosis, treatment, or clinical decision-making.

## License

This project is licensed under the **MIT License**.
