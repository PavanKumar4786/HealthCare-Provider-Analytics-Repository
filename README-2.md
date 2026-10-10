# Healthcare Provider Analytics Repository

## Project Overview

This project compares hospital-level healthcare data for **Apollo Hospitals** and **KIMS Hospitals** using Python, PySpark, Spark SQL, Pandas, and Plotly.

The workflow loads two CSV datasets, calculates selected operational and cost metrics, writes the results to an `insights.csv` file, and creates interactive visual comparisons. The analysis is intended to demonstrate how structured healthcare data can be transformed into metrics that support hospital performance review.

> **Scope note:** The current code shown in the repository reads CSV files and generates a set of comparative insights. It is not evidence of a live hospital system or a real-time data feed.

## Project Objectives

- Compare the number of patient records in the Apollo and KIMS datasets.
- Compare dermatology readmission counts.
- Compare the variance of treatment costs.
- Find minimum and maximum treatment costs for each hospital.
- Calculate the percentage of records with an outcome of `Discharged`.
- Compare the number of treatments costing more than ₹1,00,000.
- Export the results to CSV and visualize selected comparisons.

## Technology Stack

- **Python** — project logic and data handling
- **PySpark / Spark SQL** — CSV loading and metric calculations
- **Pandas** — working with the generated insights CSV
- **Plotly** — interactive comparison charts
- **Tabulate** — formatted terminal output
- **CSV** — input datasets and exported results

## Repository Structure

The following structure reflects the files visible in the repository screenshots. Keep any additional folders or files already present in your repository.

```text
HealthCare-Provider-Analytics-Repository/
└── spark/
    └── examples/
        ├── Apollo.csv
        ├── KIMS.csv
        ├── ETL.py
        ├── Visualization.py
        └── Hospital_Insights/
            └── insights.csv
```

## Input Datasets

Both supplied datasets contain **9 columns**.

| Column | Description |
|---|---|
| `Hospital_Name` | Hospital name associated with the record |
| `Patient_ID` | Patient identifier |
| `Department` | Hospital department |
| `Doctor_ID` | Doctor identifier |
| `Appointment_Date` | Appointment date |
| `Diagnosis` | Recorded diagnosis |
| `Treatment_Cost` | Treatment cost |
| `Stay_Duration` | Length of stay recorded for the patient |
| `Outcome` | Recorded outcome, such as `Discharged` or `Readmitted` |

Dataset sizes supplied with the project:

| Dataset | Records | Columns |
|---|---:|---:|
| Apollo.csv | 1,712 | 9 |
| KIMS.csv | 1,964 | 9 |
| **Total** | **3,676** | **9 per dataset** |

These are the row counts in the supplied CSV files, not a claim about the hospitals' real-world patient populations.

## Workflow

### 1. Load data

`ETL.py` starts a Spark session and reads the Apollo and KIMS CSV files with headers and schema inference enabled. It registers the datasets as temporary views for SQL queries.

### 2. Calculate comparative insights

The visible ETL code calculates:

1. **Patient volume** — compares the number of rows in each dataset.
2. **Dermatology readmissions** — counts records in the Dermatology department whose outcome is `Readmitted`.
3. **Treatment-cost variance** — compares the variance of `Treatment_Cost` in the two datasets.
4. **Minimum and maximum treatment costs** — calculates each hospital dataset's lowest and highest recorded treatment costs.
5. **Discharge rate** — calculates the percentage of records whose outcome is `Discharged`.
6. **High-cost treatments** — counts records with `Treatment_Cost` greater than ₹1,00,000.

The results are assembled into a common insights table with columns for the insight name, Apollo value, KIMS value, and conclusion.

### 3. Export results

The ETL script exports the generated insights to:

```text
Hospital_Insights/insights.csv
```

### 4. Visualize results

`Visualization.py` reads `Hospital_Insights/insights.csv` using Pandas and uses Plotly to display comparison charts. The visible code includes charts for:

- Patient volume
- Dermatology readmissions
- Treatment-cost variance
- Apollo minimum and maximum costs
- KIMS minimum and maximum costs
- Discharge rate
- High-cost treatments

The chart windows are displayed using Plotly's `fig.show()`.

## Results Included in the Repository

The committed `insights.csv` preview shows these values:

| Metric | Apollo | KIMS |
|---|---:|---:|
| Patient volume (rows) | 1,712 | 1,964 |
| Dermatology readmissions | 99 | 93 |
| Discharge rate | 32.24% | 33.91% |
| Treatments costing more than ₹1 lakh | 623 | 683 |
| Minimum treatment cost | ₹5,018.41 | ₹5,037.71 |
| Maximum treatment cost | ₹149,854.75 | ₹149,984.36 |

The output also includes treatment-cost variance. Interpret variance in the context of the code and the dataset; it measures dispersion and should not be described as the average cost.

**Important interpretation notes:**
- The patient-volume comparison counts dataset rows; it does not establish unique patient counts unless `Patient_ID` uniqueness is checked.
- The readmission metric shown here is limited to the Dermatology department, not all departments.
- The discharge rate uses all rows in each dataset as its denominator and counts rows whose outcome is exactly `Discharged`.
- These figures describe the supplied datasets and should not be treated as verified clinical quality indicators or causal evidence of hospital performance.

## Setup and Execution

The original `ETL.py` screenshot contains Windows-specific Java, Spark, and CSV paths. Update those paths to match your computer or Databricks environment before running the script.

### Prerequisites

- Python
- Java compatible with the installed Spark version
- PySpark
- Pandas
- Plotly
- Tabulate

Install the Python dependencies:

```bash
pip install pyspark pandas plotly tabulate
```

### Step 1: Place the files

Keep `ETL.py`, `Visualization.py`, `Apollo.csv`, and `KIMS.csv` in the expected project directory, or update the paths in the scripts.

### Step 2: Run the ETL script

From the directory containing `ETL.py`, run:

```bash
python ETL.py
```

The script should load the datasets, calculate the configured metrics, and write `Hospital_Insights/insights.csv` if the environment and paths are configured correctly.

### Step 3: Run the visualizations

After the insights CSV has been generated, run:

```bash
python Visualization.py
```

Plotly will open the configured charts in the available display or browser environment.

> The repository code uses Spark APIs and Windows-specific paths in the screenshot. The commands above are general execution guidance; successful execution depends on configuring Java, Spark, and all paths for your environment.

## Limitations and Future Improvements

- Use relative paths or configuration variables instead of hard-coded machine-specific paths.
- Add automated data-quality checks for missing values, duplicate patient identifiers, invalid dates, and out-of-range costs.
- Clarify whether metrics should use row counts or distinct patients.
- Calculate readmission rates with an explicitly defined denominator and time window.
- Add automated tests and sample output screenshots.
- Add a dependency file such as `requirements.txt`.
- If live or scheduled ingestion is intended, implement and document that separately; the currently visible workflow processes CSV files.

## Author

**Pavan Kumar Reddy Yarrabolu**

GitHub: [PavanKumar4786](https://github.com/PavanKumar4786)

Repository: [HealthCare-Provider-Analytics-Repository](https://github.com/PavanKumar4786/HealthCare-Provider-Analytics-Repository)
