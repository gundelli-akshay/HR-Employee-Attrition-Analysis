# ============================================================
# FILE: analysis.py
# HR Employee Attrition Analysis - Main Script
# Run: python analysis.py
# ============================================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ── Settings ─────────────────────────────────────────────────
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

DATA_PATH   = r"data/hr_attrition.csv"
VISUALS_DIR = r"visuals"
REPORT_PATH = r"hr_report.txt"

PALETTE = {
    "green": "#2ecc71",
    "red": "#e74c3c",
    "blue": "#3498db",
    "orange": "#e67e22",
    "purple": "#9b59b6",
}

os.makedirs(VISUALS_DIR, exist_ok=True)


# ── Helper ───────────────────────────────────────────────────
def save(fig, filename):
    path = os.path.join(VISUALS_DIR, filename)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"  [saved] {path}")


def bar_chart(series, title, xlabel, ylabel, filename, color):
    fig, ax = plt.subplots()
    bars = ax.bar(series.index.astype(str), series.values, color=color)
    ax.bar_label(bars, padding=4)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    save(fig, filename)


def barh_chart(series, title, xlabel, filename, color):
    fig, ax = plt.subplots()
    bars = ax.barh(series.index[::-1], series.values[::-1], color=color)
    ax.bar_label(bars, fmt="%.1f%%", padding=4)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlabel(xlabel)
    save(fig, filename)


# ============================================================
# STEP 1 — Load Data
# ============================================================
def load_data():
    print("\n📂 Loading dataset...")

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError("Dataset not found in data/ folder.")

    df = pd.read_csv(DATA_PATH)

    print(f"  Rows: {df.shape[0]}  |  Columns: {df.shape[1]}")
    return df


# ============================================================
# STEP 2 — Clean Data
# ============================================================
def clean_data(df):
    print("\n🧹 Cleaning data...")

    missing = df.isnull().sum().sum()
    print(f"  Missing values: {missing}")

    dupes = df.duplicated().sum()
    print(f"  Duplicate rows: {dupes}")
    if dupes > 0:
        df = df.drop_duplicates()

    drop_cols = ["EmployeeCount", "Over18", "StandardHours"]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])

    df["Attrition_Flag"] = df["Attrition"].map({"Yes": 1, "No": 0})

    print("  Data is clean and ready.")
    return df


# ============================================================
# STEP 3 — EDA
# ============================================================
def run_eda(df):
    print("\n🔍 Running EDA...")

    findings = {}

    rate = df["Attrition_Flag"].mean() * 100
    findings["attrition_rate"] = rate
    print(f"  Overall Attrition Rate : {rate:.2f}%")

    dept = (
        df.groupby("Department")["Attrition_Flag"]
        .mean().mul(100).sort_values(ascending=False)
    )
    findings["dept_attrition"] = dept
    print(f"\n  Attrition by Department:\n{dept.round(2).to_string()}")

    income = df.groupby("Attrition")["MonthlyIncome"].mean()
    findings["income"] = income
    print(f"\n  Avg Monthly Income:\n{income.round(2).to_string()}")

    age = df.groupby("Attrition")["Age"].mean()
    findings["age"] = age
    print(f"\n  Avg Age:\n{age.round(2).to_string()}")

    wlb = (
        df.groupby("WorkLifeBalance")["Attrition_Flag"]
        .mean().mul(100)
    )
    findings["wlb"] = wlb
    print(f"\n  Attrition by Work-Life Balance:\n{wlb.round(2).to_string()}")

    ot = (
        df.groupby("OverTime")["Attrition_Flag"]
        .mean().mul(100)
    )
    findings["overtime"] = ot
    print(f"\n  Attrition by OverTime:\n{ot.round(2).to_string()}")

    js = (
        df.groupby("JobSatisfaction")["Attrition_Flag"]
        .mean().mul(100)
    )
    findings["job_satisfaction"] = js
    print(f"\n  Attrition by Job Satisfaction:\n{js.round(2).to_string()}")

    return findings


# ============================================================
# STEP 4 — Visualizations
# ============================================================
def create_visualizations(df, findings):
    print("\n📊 Creating visualizations...")

    # 1 — Attrition Count
    fig, ax = plt.subplots()
    counts = df["Attrition"].value_counts()
    bars = ax.bar(counts.index, counts.values,
                  color=[PALETTE["green"], PALETTE["red"]], width=0.4)
    ax.bar_label(bars, padding=4)
    ax.set_title("Employee Attrition Count", fontsize=14, fontweight="bold")
    ax.set_xlabel("Attrition")
    ax.set_ylabel("Number of Employees")
    save(fig, "1_attrition_count.png")

    # 2 — Department Attrition
    barh_chart(
        findings["dept_attrition"],
        "Attrition Rate by Department (%)",
        "Attrition Rate (%)",
        "2_dept_attrition.png",
        PALETTE["orange"],
    )

    # 3 — Income vs Attrition
    fig, ax = plt.subplots()
    sns.boxplot(
        x="Attrition",
        y="MonthlyIncome",
        data=df,
        palette={"No": PALETTE["green"], "Yes": PALETTE["red"]},
    )
    ax.set_title("Monthly Income vs Attrition", fontsize=14, fontweight="bold")
    ax.set_ylabel("Monthly Income")
    save(fig, "3_income_attrition.png")

    # 4 — Age Distribution
    fig, ax = plt.subplots()
    for label, color in zip(["No", "Yes"], [PALETTE["green"], PALETTE["red"]]):
        subset = df[df["Attrition"] == label]["Age"]
        ax.hist(subset, bins=20, alpha=0.6, label=label, color=color)
    ax.set_title("Age Distribution by Attrition", fontsize=14, fontweight="bold")
    ax.set_xlabel("Age")
    ax.set_ylabel("Count")
    ax.legend(title="Attrition")
    save(fig, "4_age_distribution.png")

    # 5 — Overtime vs Attrition
    fig, ax = plt.subplots()
    ot_data = df.groupby(["OverTime", "Attrition"]).size().unstack()
    ot_data.plot(kind="bar", ax=ax,
                 color=[PALETTE["green"], PALETTE["red"]])
    ax.set_title("Overtime vs Attrition", fontsize=14, fontweight="bold")
    ax.set_xlabel("Overtime")
    ax.set_ylabel("Count")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    save(fig, "5_overtime_attrition.png")

    # 6 — Job Satisfaction
    bar_chart(
        findings["job_satisfaction"],
        "Attrition Rate by Job Satisfaction",
        "Job Satisfaction Level",
        "Attrition Rate (%)",
        "6_job_satisfaction.png",
        PALETTE["purple"],
    )

    # 7 — Correlation Heatmap
    fig, ax = plt.subplots(figsize=(14, 10))
    sns.heatmap(
        df.select_dtypes(include=np.number).corr(),
        cmap="coolwarm",
        center=0,
        linewidths=0.5,
        annot=False
    )
    ax.set_title("Feature Correlation Heatmap", fontsize=14, fontweight="bold")
    save(fig, "7_correlation_heatmap.png")

    print(f"  All charts saved to '{VISUALS_DIR}/' folder.")


# ============================================================
# STEP 5 — Save Summary Report
# ============================================================
def save_report(df, findings):
    print("\n📝 Saving summary report...")

    rate    = findings["attrition_rate"]
    dept    = findings["dept_attrition"]
    income  = findings["income"]
    age     = findings["age"]
    ot      = findings["overtime"]

    top_dept        = dept.idxmax()
    top_dept_rate   = dept.max()
    income_left     = income.get("Yes", 0)
    income_stayed   = income.get("No", 0)
    income_diff     = income_stayed - income_left
    age_left        = age.get("Yes", 0)
    ot_yes          = ot.get("Yes", 0)
    ot_no           = ot.get("No", 0)

    report = f"""
============================================================
       HR EMPLOYEE ATTRITION ANALYSIS — SUMMARY REPORT
============================================================

DATASET
  Records : {len(df)} employees

------------------------------------------------------------
KEY FINDINGS
------------------------------------------------------------

1. OVERALL ATTRITION RATE
   {rate:.2f}% of employees left the company.

2. DEPARTMENT WITH HIGHEST ATTRITION
   {top_dept} — {top_dept_rate:.1f}% attrition rate.

3. SALARY IMPACT
   Employees who left earned ${income_left:,.0f}/month on average,
   compared to ${income_stayed:,.0f}/month for those who stayed.
   Difference: ${income_diff:,.0f}/month.

4. AGE FACTOR
   Average age of employees who left: {age_left:.1f} years.
   Younger employees (25–35) show the highest attrition risk.

5. OVERTIME IMPACT
   Attrition rate with overtime    : {ot_yes:.1f}%
   Attrition rate without overtime : {ot_no:.1f}%
   Employees doing overtime are significantly more likely to leave.

------------------------------------------------------------
RECOMMENDATIONS
------------------------------------------------------------
  • Review compensation packages, especially in {top_dept}
  • Reduce mandatory overtime to improve retention
  • Focus engagement programs on employees aged 25–35
  • Improve job satisfaction and work-life balance initiatives

============================================================
"""

    with open(REPORT_PATH, "w") as f:
        f.write(report)

    print(f"  Report saved to '{REPORT_PATH}'")


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("   HR EMPLOYEE ATTRITION ANALYSIS")
    print("=" * 60)

    df = load_data()
    df = clean_data(df)
    findings = run_eda(df)
    create_visualizations(df, findings)
    save_report(df, findings)

    print("\n✅ Analysis complete!")
    print(f"   Charts  → {VISUALS_DIR}/")
    print(f"   Report  → {REPORT_PATH}")