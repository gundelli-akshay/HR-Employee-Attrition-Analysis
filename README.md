# HR Employee Attrition Analysis

A data analysis project to find out why employees leave a company, using Python and the IBM HR Analytics dataset.

---

## What This Project Does

* Loads and cleans HR employee data
* Analyzes attrition patterns across departments, salary, age, and overtime
* Creates 7 charts to visualize key findings
* Generates a summary report with recommendations

---

## Dataset

* Source: IBM HR Analytics Dataset from Kaggle
* Link: https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset
* 1,470 employee records
* 35 columns
* Target column: Attrition (Yes or No)

---

## Tools Used

* Python 3.8+
* Pandas
* NumPy
* Matplotlib
* Seaborn
* VS Code

---

## Project Structure

```
hr-employee-attrition-analysis/
├── data/
│   └── hr_attrition.csv
├── visuals/
│   ├── 1_attrition_count.png
│   ├── 2_dept_attrition.png
│   ├── 3_income_attrition.png
│   ├── 4_age_distribution.png
│   ├── 5_overtime_attrition.png
│   ├── 6_job_satisfaction.png
│   └── 7_correlation_heatmap.png
├── analysis.py
├── hr_attrition_report.txt
└── README.md
```

---

## How to Run

Step 1 - Clone the repository
```bash
git clone https://github.com/your-username/hr-attrition-analysis.git
cd hr-attrition-analysis
```

Step 2 - Install required libraries
```bash
pip install pandas numpy matplotlib seaborn
```

Step 3 - Download the dataset from Kaggle
* Rename the file to hr_attrition.csv
* Place it inside the data/ folder

Step 4 - Run the script
```bash
python analysis.py
```

---

## Key Findings

* Overall attrition rate is around 16%
* Sales department has the highest attrition at around 20%
* Employees who left earned about $2,000 less per month than those who stayed
* Younger employees between age 25 and 35 are most likely to leave
* Employees working overtime leave at a much higher rate
* Employees with low job satisfaction score of 1 have the highest attrition

---

## Recommendations

* Review salaries especially in the Sales department
* Reduce overtime to improve employee retention
* Focus retention efforts on younger employees
* Improve job satisfaction through better growth opportunities

---

## Skills Demonstrated

* Data cleaning and preparation
* Exploratory data analysis
* Data visualization
* Business insight generation
* Python scripting with modular functions

---

## Author

Name: Akshay Gundelli

Email: gundelliakshay@gmail.com

LinkedIn: https://linkedin.com/in/gundelli-akshay

GitHub: https://github.com/gundelli-akshay

---

## License

This project is open source under the MIT License.

