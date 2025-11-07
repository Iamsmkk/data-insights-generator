# Data Insights Generator – Core Python Edition

This is a simple Python project that analyzes a dataset (CSV format) and generates a text-based report with key insights such as averages, minimums, maximums, and category frequencies.  
It is built entirely using **core Python** — no external libraries required.

---

## 📘 How It Works
1. The program reads the CSV file stored in the `data` folder.  
2. It detects numeric columns and calculates average, minimum, and maximum values.  
3. It identifies the most frequent value in the first categorical column.  
4. It checks for missing values in the dataset.  
5. It generates a summary report saved as `sample_output.txt`.

---

## 🧠 Concepts Used
- File I/O (`open`, `read`, `write`)
- CSV parsing with the `csv` module
- Loops and conditionals
- Dictionaries and lists
- Functions for modular code
- Basic statistics (average, min, max)
- Error handling

---

## ⚙️ How to Run
1. Place your dataset in the `data` folder (or use the provided `sales_data.csv`).
2. Run the program:
   ```bash
   python insights_generator.py
