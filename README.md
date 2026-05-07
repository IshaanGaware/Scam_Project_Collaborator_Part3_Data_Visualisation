Scammed Young - Data Visualisation Project
Project Contact Information:
• Name: Aryan Goel
• Student ID: 26040826
• Student Email: Aryan.goel-1@student.uts.edu.au
Contribution 1: 
1. Data Processing & Metric Creation
• Helper Functions: I added functions like money_to_float and standardise_state_name to clean and standardize the Scamwatch dataset.
• Target Demographic: I successfully filtered the primary dataset to isolate data for young adults aged 18-24 (young_df).
• Population Normalization: I loaded ABS population data, aggregated it to the state level, and merged it with my scam data. This allowed me to calculate valuable normalized metrics: reports_per_100k_young, losses_per_100k_young, and avg_loss_per_report.
2. Exploratory Data Analysis & Visualizations
I added several useful visualizations to understand the impact of scams:
• Monthly Trends: I created a line plot showing the monthly scam reports for young adults throughout 2025.
• Scam Categories: I calculated aggregate losses by category and built a horizontal bar chart for the "Top Scam Categories by Losses," revealing that Threat scams and Job/employment scams are leading the financial impact.
• Contact Modes: I used a pivot table to generate a stacked bar chart illustrating how different age groups are contacted by scammers (e.g., Email, Online, Phone call).
3. ACMA Dataset Integration (New Additions & Errors)
I added a substantial block dedicated to loading and cleaning the ACMA Context Dataset.
• Cleaning Steps Added: Standardizing column names, removing duplicates, and handling missing values by replacing numeric NaNs with the median and categorical NaNs with "Unknown".
• EDA Visualizations Added: I wrote code to generate bar charts for missing values, histograms for distributions, a correlation matrix, and boxplots for outlier detection.
• ⚠️ Action Required - Import Error: My initial pd.read_excel(ACMA_FILE) throws a ValueError: Excel file format cannot be determined, you must specify an engine manually. I may need to specify engine='openpyxl' depending on the file type.
• ⚠️ Action Required - Correlation Matrix Error: During the plotting phase, the line corr = acma_df[numeric_cols].corr() throws a ValueError: Cannot mask with non-boolean array containing NA / NaN values. This typically happens if numeric_cols accidentally captured columns with incompatible types or unhandled missing values that the correlation function cannot process.
4. Data Export
• File Generation: I successfully added an export routine at the end of the notebook to save my cleaned datasets (scamwatch_clean.csv, state_summary.csv, category_summary.csv, and contact_age_summary.csv) into a designated output directory.

----------------------------------------------------------------------------------------------------------------------------------------