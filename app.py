import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.charts import (
    create_risk_distribution_chart,
    create_vital_trend_chart,
)

from src.data_loader import load_clinical_data

from src.metrics import (
    calculate_patient_metrics,
    get_patient_summary,
    get_patient_vitals,
)


# ==============================================================================
# PAGE CONFIGURATION
# ==============================================================================

st.set_page_config(
    page_title="Clinical Metrics Dashboard",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ==============================================================================
# CUSTOM CSS
# ==============================================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-color: #070B11;
        color: #E2E8F0;
    }

    [data-testid="stHeader"] {
        background-color: transparent !important;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    .section-header {
        color: #38BDF8;
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 1.8rem;
        margin-bottom: 1rem;
        padding-bottom: 0.4rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }

    .metric-box {
        background: #0F172A;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 16px 18px;
        height: 115px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        transition: border-color 0.2s ease;
    }

    .metric-box:hover {
        border-color: rgba(56, 189, 248, 0.4);
    }

    .metric-label {
        color: #64748B;
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    .metric-value {
        color: #FFFFFF;
        font-size: 1.35rem;
        font-weight: 700;
        line-height: 1.2;
    }

    div[data-baseweb="select"] > div, 
    div[data-baseweb="base-input"],
    .stTextArea textarea {
        background-color: #0F172A !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 8px !important;
        color: #FFFFFF !important;
    }

    div[data-baseweb="slider"] div {
        background-color: #38BDF8 !important;
    }

    .status-badge-container {
        margin-top: 4px;
    }

    .status-badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.05em;
    }

    .badge-above {
        background-color: rgba(239, 68, 68, 0.2);
        color: #F87171;
        border: 1px solid rgba(239, 68, 68, 0.4);
    }

    .badge-below {
        background-color: rgba(16, 185, 129, 0.2);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.4);
    }

    /* Enhanced Critical Alert Box Styling */
    .critical-alert-card {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(127, 29, 29, 0.25) 100%);
        border: 1px solid rgba(239, 68, 68, 0.4);
        border-left: 4px solid #EF4444;
        border-radius: 10px;
        padding: 14px 20px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.08);
    }

    .alert-header-title {
        color: #F87171;
        font-size: 0.9rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
        letter-spacing: 0.03em;
    }

    .alert-badge-count {
        background: #EF4444;
        color: #FFFFFF;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 12px;
    }

    .alert-patient-badges {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        align-items: center;
        margin-top: 6px;
    }

    .patient-chip {
        background: rgba(239, 68, 68, 0.2);
        border: 1px solid rgba(239, 68, 68, 0.4);
        color: #FCA5A5;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 6px;
        letter-spacing: 0.03em;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def section_title(title: str) -> None:
    st.markdown(
        f'<div class="section-header">{title}</div>',
        unsafe_allow_html=True,
    )


def metric_box(
    label: str,
    value: str,
    badge_type: str = None,
    badge_label: str = None,
) -> None:
    badge_html = ""
    if badge_type and badge_label:
        badge_html = f'<div class="status-badge-container"><span class="status-badge badge-{badge_type}">{badge_label}</span></div>'
    else:
        badge_html = '<div style="height: 18px;"></div>'

    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            {badge_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def create_risk_gauge_chart(risk_score: float):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=risk_score,
            number={"suffix": "%", "font": {"color": "#FFFFFF", "size": 32}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#64748B"},
                "bar": {"color": "#38BDF8"},
                "bgcolor": "#0F172A",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 30], "color": "rgba(16, 185, 129, 0.25)"},
                    {"range": [30, 70], "color": "rgba(245, 158, 11, 0.25)"},
                    {"range": [70, 100], "color": "rgba(239, 68, 68, 0.25)"},
                ],
            },
        )
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        height=180,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


# ==============================================================================
# LOAD DATA
# ==============================================================================

try:
    patients, vitals = load_clinical_data()
except (FileNotFoundError, ValueError) as exc:
    st.error(f"Unable to load clinical data: {exc}")
    st.stop()

if patients.empty or vitals.empty:
    st.error("Clinical dataset is empty.")
    st.stop()


# ==============================================================================
# SESSION STATE
# ==============================================================================

patient_options = patients["patient_id"].tolist()

if (
    "selected_patient" not in st.session_state
    or st.session_state.selected_patient not in patient_options
):
    st.session_state.selected_patient = patient_options[0]

if "risk_threshold" not in st.session_state:
    st.session_state.risk_threshold = 50

if "patient_notes" not in st.session_state:
    st.session_state.patient_notes = {}


# ==============================================================================
# HEADER
# ==============================================================================

st.title("Clinical Metrics Dashboard")
st.caption(
    "Synthetic clinical data for dashboard demonstration. "
    "This application is not a clinical decision-support system."
)


# ==============================================================================
# CRITICAL PATIENTS HIGH-RISK ALERT (UPDATED BEAUTIFIED UI)
# ==============================================================================

high_risk_patients = patients[patients["readmission_risk_score"] >= 0.70]

if not high_risk_patients.empty:
    patient_badges_html = "".join(
        [
            f'<span class="patient-chip">{p_id}</span>'
            for p_id in high_risk_patients["patient_id"]
        ]
    )

    st.markdown(
        f"""
        <div class="critical-alert-card">
            <div class="alert-header-title">
                <span> CRITICAL ATTENTION REQUIRED</span>
                <span class="alert-badge-count">{len(high_risk_patients)} Patients</span>
                <span style="color: #94A3B8; font-size: 0.8rem; font-weight: 400; margin-left: 6px;">(Readmission Risk &ge; 70%)</span>
            </div>
            <div class="alert-patient-badges">
                <span style="color: #CBD5E1; font-size: 0.8rem; font-weight: 500; margin-right: 4px;">High Risk Patient IDs:</span>
                {patient_badges_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==============================================================================
# DASHBOARD OVERVIEW
# ==============================================================================

section_title("Dashboard Overview")

overview = st.columns(4)

with overview[0]:
    metric_box("Total Patients", str(len(patients)))

with overview[1]:
    metric_box("Total Visits", str(len(vitals)))

with overview[2]:
    metric_box("Average Age", f"{patients['age'].mean():.1f} yrs")

with overview[3]:
    metric_box(
        "Average Risk",
        f"{patients['readmission_risk_score'].mean() * 100:.1f}%",
    )


# ==============================================================================
# RISK DISTRIBUTION
# ==============================================================================

section_title("Risk Distribution")

risk_distribution = (
    patients["readmission_risk_score"]
    .apply(
        lambda score: (
            "Low" if score < 0.30 else "Moderate" if score < 0.70 else "High"
        )
    )
    .value_counts()
    .reindex(["Low", "Moderate", "High"], fill_value=0)
)

risk_chart_col, risk_count_col = st.columns([2, 1])

with risk_chart_col:
    risk_figure = create_risk_distribution_chart(patients)
    st.plotly_chart(
        risk_figure,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "displaylogo": False,
            "responsive": True,
        },
    )

with risk_count_col:
    metric_box("Low Risk Patients", str(risk_distribution["Low"]))
    st.write("")
    metric_box("Moderate Risk Patients", str(risk_distribution["Moderate"]))
    st.write("")
    metric_box("High Risk Patients", str(risk_distribution["High"]))


# ==============================================================================
# PATIENT SELECTION & FILTERS
# ==============================================================================

section_title("Patient Selection & Filters")

patient_labels = {
    row["patient_id"]: (
        f"{row['patient_id']} — {row['gender']} — Age {int(row['age'])}"
    )
    for _, row in patients.iterrows()
}

filter_col1, filter_col2 = st.columns([2, 1])

with filter_col1:
    selected_patient = st.selectbox(
        "Select Patient Profile",
        options=patient_options,
        format_func=lambda patient_id: patient_labels[patient_id],
        key="selected_patient",
    )

with filter_col2:
    risk_threshold = st.slider(
        "Risk Threshold Parameter",
        min_value=0,
        max_value=100,
        step=5,
        format="%d%%",
        key="risk_threshold",
    )

patient = get_patient_summary(patients, selected_patient)
patient_vitals = get_patient_vitals(vitals, selected_patient).copy()
patient_vitals["visit_date"] = pd.to_datetime(patient_vitals["visit_date"])

min_date = patient_vitals["visit_date"].min().date()
max_date = patient_vitals["visit_date"].max().date()

st.write("")

info_col1, info_col2, info_col3 = st.columns([1, 1, 1])

with info_col1:
    metric_box("Patient ID", str(selected_patient))

with info_col2:
    metric_box("Gender", str(patient["gender"]))

with info_col3:
    metric_box("Age", f"{int(patient['age'])} Years")

st.write("")

date_col, visit_count_col = st.columns([2, 1])

with date_col:
    selected_dates = st.date_input(
        "Select Visit Date Range",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        key=f"date_range_{selected_patient}",
    )

if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
    start_date, end_date = selected_dates
    filtered_vitals = patient_vitals[
        (patient_vitals["visit_date"].dt.date >= start_date)
        & (patient_vitals["visit_date"].dt.date <= end_date)
    ].copy()
elif isinstance(selected_dates, tuple):
    filtered_vitals = patient_vitals.copy()
else:
    filtered_vitals = patient_vitals[
        patient_vitals["visit_date"].dt.date == selected_dates
    ].copy()

with visit_count_col:
    metric_box("Visits in Period", str(len(filtered_vitals)))


# ==============================================================================
# CURRENT PATIENT METRICS
# ==============================================================================

section_title("Current Patient Metrics")

if not filtered_vitals.empty:
    latest_filtered_visit = filtered_vitals.sort_values("visit_date").iloc[-1]
else:
    latest_filtered_visit = patient_vitals.sort_values("visit_date").iloc[-1]

blood_pressure = (
    f"{latest_filtered_visit['systolic_bp']:.1f}/"
    f"{latest_filtered_visit['diastolic_bp']:.1f} mmHg"
)
glucose = f"{latest_filtered_visit['glucose']:.1f} mg/dL"

patient_metrics = calculate_patient_metrics(patient, patient_vitals)
risk_score = float(patient_metrics["risk_score"])
risk_level = str(patient_metrics["risk_level"])

is_above = risk_score >= risk_threshold
status_badge = "above" if is_above else "below"
status_text = "Above Threshold" if is_above else "Below Threshold"

metric_columns = st.columns(5)

with metric_columns[0]:
    metric_box("Blood Pressure", blood_pressure)

with metric_columns[1]:
    metric_box("Glucose", glucose)

with metric_columns[2]:
    metric_box("Readmission Risk", f"{risk_score:.1f}%")

with metric_columns[3]:
    metric_box("Risk Level", risk_level)

with metric_columns[4]:
    metric_box(
        "Threshold Status",
        status_text,
        badge_type=status_badge,
        badge_label="ALERT" if is_above else "NORMAL",
    )


# ==============================================================================
# RISK THRESHOLD ANALYSIS & GAUGE
# ==============================================================================

section_title("Risk Threshold Analysis & Gauge Meter")

analysis_col1, analysis_col2 = st.columns([1.5, 1])

with analysis_col1:
    gauge_chart = create_risk_gauge_chart(risk_score)
    st.plotly_chart(gauge_chart, use_container_width=True)

with analysis_col2:
    st.metric("Selected Risk Threshold", f"{risk_threshold}%")
    if is_above:
        st.error("⚠️ Patient risk score exceeds the selected safety threshold.")
    else:
        st.success("✓ Patient risk score is within acceptable threshold limits.")


# ==============================================================================
# CLINICAL NOTES & OBSERVATIONS
# ==============================================================================

section_title("Clinical Notes & Observations")

current_note = st.session_state.patient_notes.get(selected_patient, "")

note_input = st.text_area(
    f"Add Clinical Notes for Patient {selected_patient}:",
    value=current_note,
    height=90,
    placeholder="Type physician notes, medications, or special observations here...",
)

if st.button("Save Clinical Note"):
    st.session_state.patient_notes[selected_patient] = note_input
    st.toast(f"Note saved successfully for Patient {selected_patient}!", icon="💾")


# ==============================================================================
# VITAL TREND ANALYSIS
# ==============================================================================

section_title("Vital Trend Analysis")

if filtered_vitals.empty:
    st.warning("No visits are available for the selected date range.")
else:
    figure = create_vital_trend_chart(filtered_vitals)
    st.plotly_chart(
        figure,
        use_container_width=True,
        config={
            "displayModeBar": True,
            "displaylogo": False,
            "responsive": True,
        },
    )


# ==============================================================================
# VISIT HISTORY
# ==============================================================================

section_title("Visit History")

if filtered_vitals.empty:
    st.info("No visit records are available for the selected period.")
else:
    table_df = filtered_vitals[
        [
            "visit_number",
            "visit_date",
            "systolic_bp",
            "diastolic_bp",
            "glucose",
        ]
    ].copy()

    table_df["visit_date"] = table_df["visit_date"].dt.strftime("%Y-%m-%d")
    table_df = table_df.rename(
        columns={
            "visit_number": "Visit #",
            "visit_date": "Visit Date",
            "systolic_bp": "Systolic BP",
            "diastolic_bp": "Diastolic BP",
            "glucose": "Glucose",
        }
    )

    st.dataframe(
        table_df,
        use_container_width=True,
        hide_index=True,
    )


# ==============================================================================
# EXPORT DATA & DISCLAIMER
# ==============================================================================

section_title("Export Data")

export_data = filtered_vitals[
    [
        "patient_id",
        "visit_number",
        "visit_date",
        "systolic_bp",
        "diastolic_bp",
        "glucose",
    ]
].copy()

export_data["visit_date"] = export_data["visit_date"].dt.strftime("%Y-%m-%d")
csv_data = export_data.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Visit Data",
    data=csv_data,
    file_name=f"{selected_patient}_visit_history.csv",
    mime="text/csv",
)

st.divider()

st.caption(
    "Disclaimer: This dashboard uses synthetic data for demonstration and development purposes only."
)