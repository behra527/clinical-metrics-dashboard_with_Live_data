import pandas as pd
import plotly.graph_objects as go


def create_vital_trend_chart(
    patient_vitals: pd.DataFrame,
) -> go.Figure:
    """Create an interactive vital-sign trend chart."""

    data = patient_vitals.copy()

    data["visit_date"] = pd.to_datetime(
        data["visit_date"]
    )

    data = data.sort_values(
        "visit_date"
    )

    figure = go.Figure()

    # Systolic BP
    figure.add_trace(
        go.Scatter(
            x=data["visit_date"],
            y=data["systolic_bp"],
            mode="lines+markers",
            name="Systolic BP",
            line=dict(width=2),
            marker=dict(size=7),
            hovertemplate=(
                "<b>%{x|%Y-%m-%d}</b>"
                "<br>Systolic BP: %{y:.1f} mmHg"
                "<extra></extra>"
            ),
        )
    )

    # Diastolic BP
    figure.add_trace(
        go.Scatter(
            x=data["visit_date"],
            y=data["diastolic_bp"],
            mode="lines+markers",
            name="Diastolic BP",
            line=dict(width=2),
            marker=dict(size=7),
            hovertemplate=(
                "<b>%{x|%Y-%m-%d}</b>"
                "<br>Diastolic BP: %{y:.1f} mmHg"
                "<extra></extra>"
            ),
        )
    )

    # Glucose
    figure.add_trace(
        go.Scatter(
            x=data["visit_date"],
            y=data["glucose"],
            mode="lines+markers",
            name="Glucose",
            yaxis="y2",
            line=dict(width=2),
            marker=dict(size=7),
            hovertemplate=(
                "<b>%{x|%Y-%m-%d}</b>"
                "<br>Glucose: %{y:.1f} mg/dL"
                "<extra></extra>"
            ),
        )
    )

    figure.update_layout(
        title="Patient Vital Sign Trends",
        xaxis=dict(
            title="Visit Date",
            type="date",
            tickformat="%b %d",
            showgrid=True,
        ),
        yaxis=dict(
            title="Blood Pressure (mmHg)",
            showgrid=True,
        ),
        yaxis2=dict(
            title="Glucose (mg/dL)",
            overlaying="y",
            side="right",
            showgrid=False,
        ),
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),
        height=480,
        margin=dict(
            l=50,
            r=50,
            t=80,
            b=50,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color="#E2E8F0",
        ),
    )

    return figure


def create_risk_distribution_chart(
    patients: pd.DataFrame,
) -> go.Figure:
    """Create a patient risk distribution chart."""

    data = patients.copy()

    data["risk_level"] = data[
        "readmission_risk_score"
    ].apply(
        lambda score: (
            "Low"
            if score < 0.30
            else "Moderate"
            if score < 0.70
            else "High"
        )
    )

    risk_order = [
        "Low",
        "Moderate",
        "High",
    ]

    risk_counts = (
        data["risk_level"]
        .value_counts()
        .reindex(
            risk_order,
            fill_value=0,
        )
    )

    figure = go.Figure()

    figure.add_trace(
        go.Bar(
            x=risk_counts.index,
            y=risk_counts.values,
            name="Patients",
            hovertemplate=(
                "<b>%{x} Risk</b>"
                "<br>Patients: %{y}"
                "<extra></extra>"
            ),
        )
    )

    figure.update_layout(
        title="Patient Risk Distribution",
        xaxis=dict(
            title="Risk Level",
            showgrid=False,
        ),
        yaxis=dict(
            title="Number of Patients",
            showgrid=True,
        ),
        height=380,
        margin=dict(
            l=50,
            r=30,
            t=70,
            b=50,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color="#E2E8F0",
        ),
        showlegend=False,
    )

    return figure