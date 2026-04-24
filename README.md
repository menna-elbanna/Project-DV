# FIFA 23 Player Statistics Dashboard - Data Preprocessing & Distribution Analysis

This repository contains the data cleaning and initial distribution analysis for the Data Visualization project. This phase focuses on preparing the raw FIFA 23 dataset for use in the Plotly Dash application.

## Summary of Work Completed (Person 1 Role)

### 1. Data Cleaning & Optimization
* **Memory Management**: Since the raw `male_players.csv` is large, I implemented a **chunk-based loading strategy** (10,000 rows per chunk) to avoid memory errors.
* **Column Selection**: Filtered the dataset from 100+ columns down to the 9 essential columns needed for the team's charts (`short_name`, `age`, `nationality_name`, `overall`, `potential`, `club_name`, `player_positions`, `wage_eur`, `value_eur`).
* **Data Integrity**: Handled missing values by dropping rows with null entries in critical fields (age, wage, position).

### 2. Feature Engineering
* **Position Grouping**: Created a `position_group` column. FIFA's granular positions (e.g., ST, LW, CAM, CB) have been mapped into four broad categories: **Forward, Midfielder, Defender, and Goalkeeper**. Use this column for any categorical analysis to ensure charts are readable.

### 3. Distribution Visualizations
* **Histogram**: Analyzed the distribution of player ages.
* **Box Plot**: Visualized wage distributions across the different position groups (capped at 250k EUR for better readability of the quartiles). (note:Due to the large size of the FIFA dataset, I have implemented data sampling for the distribution visualizations. This ensures the dashboard remains responsive and prevents memory crashes while maintaining a statistically accurate representation of the player population.)

---

## Instructions for Teammates (Next Steps)

### 1. Data Setup (Crucial)
Because the data files are too large for GitHub/Email, you must set them up locally:
1.  Ensure you have the raw `male_players.csv` in your `data/` folder.
2.  pip install -r requirements.txt
3.  **Run the `preprocessing.ipynb` notebook**: This will generate the `cleaned_data.csv` on your machine.
4.  **Use `cleaned_data.csv`**: Every teammate should import this file for their Plotly charts to ensure consistency in data types and position names.

### 2. Moving to the Backend (Person 6)
* **Loading**: Load the data using `pd.read_csv('data/cleaned_data.csv')`.
* **Callbacks**: The Plotly Express code for the Histogram and Box Plot is ready in the notebook. You can copy the `px.histogram` and `px.box` definitions directly into your Dash callback functions.

### 3. UI and Comparison Charts (Persons 2, 3, 4, 5)
* **Position Filtering**: If you are creating comparison charts by position, use the `position_group` column instead of `player_positions`.
* **Styling**: Please maintain the color scheme used in the distribution charts for a consistent dashboard look.

---

## Requirements
* Pandas
* Plotly
* Jupyter Notebook