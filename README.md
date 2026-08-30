# Workshop-1: From Business Requirements to a Dimensional Data Warehouse

> ⚠️ This README is a work in progress. It currently covers business requirements, requirements traceability, and initial data profiling. Remaining sections (dimensional model, ETL pipeline, Data Warehouse implementation, analytical queries, BI visualization, and final validation) will be added as the project progresses.

## 🎯 Project Objective

Design and implement a dimensional Data Warehouse that transforms raw candidate application data from a technical recruitment process into an analytical system capable of supporting hiring-related business decisions, following a full Business Requirements → Data Understanding → Dimensional Modeling → ETL → Data Warehouse → Analytics → Business Decisions workflow.

## 🏢 Business Context

A technology recruitment company wants to improve its understanding of its candidate selection process. The company receives thousands of applications from candidates with different professional backgrounds, experience levels, countries, seniority levels, and technology profiles. Each candidate is evaluated using two technical assessments: a **Code Challenge Score** and a **Technical Interview Score**. The data is currently available only as raw files, so the organization needs an analytical system that allows decision-makers to understand hiring patterns and evaluate recruitment performance from multiple perspectives.

**Hiring business rule:**

```
HIRED = (Code Challenge Score >= 7) AND (Technical Interview Score >= 7)
Otherwise: NOT HIRED
```

## 📋 Business Requirements

| ID | Business Requirement |
|---|---|
| R1 | **Hiring Trends** — Monitor hiring trends over time to identify changes in recruitment outcomes across different periods. |
| R2 | **Technology Analysis** — Compare hiring results across technologies to identify which technical profiles generate the largest number and proportion of hired candidates. |
| R3 | **Candidate Profile Analysis** — Analyze hiring outcomes according to candidate seniority and years of professional experience. |
| R4 | **Geographic Recruitment Analysis** *(proposed)* — Identify countries with the highest application volume and compare their hiring rates to support geographic recruitment strategy. |
| R5 | **Technical Assessment Effectiveness** *(proposed)* — Analyze the relationship between the Code Challenge Score and the Technical Interview Score to identify which assessment better discriminates between hired and not-hired candidates. |

### Requirements Traceability

| Requirement | Business Question | Data Required | Expected Analytical Output |
|---|---|---|---|
| R1 | How do applications and hires change over time? | Application Date, Hired (derived) | Time series of applications and hires by month/year |
| R2 | Which technologies generate the most hired candidates, in number and proportion? | Technology, Hired (derived) | Ranking of technologies by count and hiring percentage |
| R3 | How does the hiring rate vary by seniority level and years of experience? | Seniority, YOE, Hired (derived) | Hiring rate by seniority level and YOE range |
| R4 | Which countries concentrate the most applications, and which show better or worse hiring rates? | Country, Hired (derived) | Ranking of countries by application volume and hiring percentage |
| R5 | Which of the two technical assessments better discriminates between HIRED and NOT HIRED candidates? | Code Challenge Score, Technical Interview Score, Hired (derived) | Comparison of average scores and distribution of each assessment between HIRED and NOT HIRED |

## 📊 Dataset Description

The source dataset (`data/raw/candidates.csv`) contains **50,000 candidate applications**, one row per application, with the following attributes: First Name, Last Name, Email, Application Date, Country, YOE (Years of Experience), Seniority, Technology, Code Challenge Score, and Technical Interview Score.

## 🔍 Main Profiling Findings (Task 1)

- **Shape:** 50,000 rows × 10 columns.
- **Missing values:** none found in any column.
- **Duplicates:** no fully duplicated rows; 167 duplicate email addresses (no duplicates when checking First Name + Last Name + Email together), indicating some candidates may have applied more than once. This will be addressed explicitly during data preparation.
- **Country:** 244 unique values.
- **Seniority:** 7 unique values (Intern, Trainee, Junior, Mid-Level, Senior, Lead, Architect), almost evenly distributed (~14% each).
- **Technology:** 24 unique values, covering roles such as Data Engineer, DevOps, Development (Backend/Frontend/FullStack/CMS), QA, Security, Business Intelligence, Sales, and more.
- **Application Date:** ranges from **2018-01-01** to **2022-07-04**, with no invalid/unparseable values.
- **YOE:** ranges from 0 to 30 years (mean ≈ 15.3).
- **Scores:** both Code Challenge Score and Technical Interview Score range from 0 to 10 (mean ≈ 5.0 each), with no out-of-range values.
- **Hiring outcome:** applying the business rule to the full dataset results in **6,698 candidates HIRED (13.4%)** and **43,302 candidates NOT HIRED (86.6%)**.

## 🛠️ Technologies

Python · Pandas · Jupyter Notebook · SQL · MySQL/PostgreSQL · Git & GitHub · BI Tool (Power BI / Tableau / Looker Studio)

## 📁 Repository Structure

```
ETL-Workshop-1/
│
├── data/
│   └── raw/
│       └── candidates.csv
│
├── notebooks/
│   ├── data_profiling.ipynb
|   └── data_profiling.py
│
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── dimensional_model.py
│   ├── load.py
│   └── main.py
│
├── sql/
│   ├── create_tables.sql
│   └── analytical_queries.sql
│
├── database/
│   └── recruitment_dw.db
│
├── diagrams/
│   └── star_schema.png
│
├── docs/
│
├── results/
│
├── README.md
├── requirements.txt
└── .gitignore
```

## 🚧 Next Steps

- Design the dimensional Star Schema (grain, dimensions, facts) and validate it against R1–R5.
- Implement the ETL pipeline (extract, prepare, transform).
- Load the Data Warehouse (MySQL/PostgreSQL).
- Generate analytical queries and KPIs.
- Build BI visualizations.
- Complete final requirements validation.

## 💡Recommendations

1. Install the extension `Jupyter` from Microsoft to run `data_profiling.ipynb` and visualize the results
2. Following above, if you want to transform a `.py` archive to `.ipynb` (or vice versa) as i did in notebooks folder, you can use the library `jupytext`
```bash
# Command
pip install jupytext
```

Afterwards, in my case i used:
```bash
# Command - This transform from .py to .ipynb and sync the changes
jupytext --set-formats ipynb,py data_profiling.py --sync
```
> You must be inside the folder.

**More info:** https://stackoverflow.com/questions/62510114/converting-from-py-to-ipynb

