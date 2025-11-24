
#  HOSPITAL INSIGHTS VISUALIZATION (PLOTLY)


import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import os


#  1. LOAD INSIGHTS CSV

csv_path = "Hospital_Insights/insights.csv"

if not os.path.exists(csv_path):
    raise FileNotFoundError("Insights CSV not found! Run insights generator first.")

insights = pd.read_csv(csv_path)

# Convert values to numeric
insights["Apollo_Value"] = pd.to_numeric(insights["Apollo_Value"], errors="coerce")
insights["KIMS_Value"]  = pd.to_numeric(insights["KIMS_Value"],  errors="coerce")

# Helper function → easy bar chart creation
def create_comparison_bar(title, x_labels, apollo_val, kims_val, y_title):
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Apollo", x=x_labels, y=apollo_val))
    fig.add_trace(go.Bar(name="KIMS",  x=x_labels, y=kims_val))
    fig.update_layout(
        title=title,
        barmode="group",
        yaxis_title=y_title,
        template="plotly_white"
    )
    fig.show()


# 2. VISUALIZATIONS

# A. Patient Volume Comparison

row = insights[insights["Insight"] == "Patient Volume"].iloc[0]
create_comparison_bar(
    title="Patient Volume Comparison",
    x_labels=["Apollo", "KIMS"],
    apollo_val=[row["Apollo_Value"]],
    kims_val=[row["KIMS_Value"]],
    y_title="Number of Patients"
)


# B. Dermatology Readmissions

row = insights[insights["Insight"] == "Dermatology Readmissions"].iloc[0]
create_comparison_bar(
    title="Dermatology Readmissions Comparison",
    x_labels=["Apollo", "KIMS"],
    apollo_val=[row["Apollo_Value"]],
    kims_val=[row["KIMS_Value"]],
    y_title="Readmissions"
)


# C. Cost Variance Comparison

row = insights[insights["Insight"] == "Cost Variance"].iloc[0]
create_comparison_bar(
    title="Cost Variance Comparison",
    x_labels=["Apollo", "KIMS"],
    apollo_val=[row["Apollo_Value"]],
    kims_val=[row["KIMS_Value"]],
    y_title="Variance"
)


# D. Apollo Min & Max Costs

apollo_mm = insights[insights["Insight"].isin(["Apollo Min Cost", "Apollo Max Cost"])]

fig = go.Figure()
fig.add_trace(go.Bar(
    x=apollo_mm["Insight"],
    y=apollo_mm["Apollo_Value"],
    name="Apollo",
    marker_color="blue"
))
fig.update_layout(
    title="Apollo Min & Max Treatment Costs",
    yaxis_title="Cost (INR)",
    template="plotly_white"
)
fig.show()

# E. KIMS Min & Max Costs

kims_mm = insights[insights["Insight"].isin(["KIMS Min Cost", "KIMS Max Cost"])]

fig = go.Figure()
fig.add_trace(go.Bar(
    x=kims_mm["Insight"],
    y=kims_mm["KIMS_Value"],
    name="KIMS",
    marker_color="orange"
))
fig.update_layout(
    title="KIMS Min & Max Treatment Costs",
    yaxis_title="Cost (INR)",
    template="plotly_white"
)
fig.show()


# F. Discharge Rate Comparison

row = insights[insights["Insight"] == "Discharge Rate (%)"].iloc[0]
create_comparison_bar(
    title="Discharge Rate (%) Comparison",
    x_labels=["Apollo", "KIMS"],
    apollo_val=[row["Apollo_Value"]],
    kims_val=[row["KIMS_Value"]],
    y_title="Percentage (%)"
)

# G. High-Cost Treatments (>1 Lakh)

row = insights[insights["Insight"] == "High-Cost Treatments (>1 Lakh)"].iloc[0]
create_comparison_bar(
    title="High-Cost Treatments (>1 Lakh)",
    x_labels=["Apollo", "KIMS"],
    apollo_val=[row["Apollo_Value"]],
    kims_val=[row["KIMS_Value"]],
    y_title="Number of High-Cost Cases"
)


