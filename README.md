# Court-Data Fetcher & Mini-Dashboard – Cuddalore District

## 🎯 Objective
Web app to fetch court case status from Cuddalore District Court using public eCourts portal.

## 🔍 Target Court
**Cuddalore District Court**  
Portal: [https://districts.ecourts.gov.in/cuddalore](https://districts.ecourts.gov.in/cuddalore)

## ⚙️ Tech Stack
- Python + Flask

- Selenium (ChromeDriver 138)
- SQLite
- HTML template (Jinja)

## ✅ Features
- Input: Case Type, Number, Filing Year
- Scrapes metadata: Parties, Filing Date, Next Hearing
- Returns recent order/judgment PDF link
- Logs all queries into SQLite database

## 🚀 How to Run
```bash
pip install -r requirements.txt
python app.py
