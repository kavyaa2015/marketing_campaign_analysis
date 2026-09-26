# Marketing Campaign Analytics — Project Report

## 1. Problem and objective

The retailer needs a single analytical solution to understand customer value, campaign acceptance, spending preferences, channel use, and underserved opportunities. The project answers who should be targeted in future campaigns and which commercial actions are supported by the historical customer data.

## 2. Data preparation and modelling

The source is a customer-level dataset: one record per `ID`. The Python cleaning pipeline converts `Dt_Customer` to a date and derives `Age`, `Total_Children`, `Total_Spend`, `Total_Purchases`, `Customer_Tenure_Days`, and `Total_Campaign_Accepted`. It also reports duplicate IDs, missing values, invalid negative values, unrealistic ages, and IQR outliers before exporting `data/processed/marketing_cleaned.csv`.

SQLite is the analytical layer. `sql/schema.sql` defines the `customers` table with `ID` as its primary key and indexes for country, response, income, age, and spend. `sql/load_data.py` loads the processed CSV, while `sql/analytical_queries.sql` contains KPIs, segment summaries, campaign analysis, an underserved-customer query, an ideal-target query, and dashboard-supporting views.

## 3. Exploratory analysis and segments

The EDA scripts examine distributions of age, income, recency, and spending; response versus income, age, products, and channels; and correlation with response. Rule-based segments are intentionally allowed to overlap:

| Segment | Rule |
|---|---|
| High income | Income > 75,000 |
| Young customer | Age < 30 |
| Campaign responder | Latest campaign response = 1 |
| High web engagement | More than 5 website visits per month |
| Family customer | At least one child or teen at home |
| High spender | Total spend at or above the 90th percentile |

This avoids forcing a valuable customer into only one label. For example, a high-income family customer can be studied in both relevant views.

## 4. Key findings

Results must always be read in the dashboard with the active filters applied. On the complete processed dataset, there are 56,000 customers and 8,265 latest-campaign responders (14.76%). The existing business-analysis export indicates an average income of approximately 57,252 and average spend of approximately 640. High-value customers have a higher response rate (about 26.04%), making them a priority for retention and premium offers.

The dashboard makes it possible to compare all six campaign acceptance flags, analyse product and channel preferences, assess countries and demographic bands, and inspect response rates alongside group sizes. It explicitly labels channel analysis as descriptive rather than causal.

## 5. Recommendations

1. Prioritise high-spend responders for retention and premium cross-sell campaigns; they combine current value with demonstrated receptiveness.
2. Use the campaign scorecard to replicate and test the strongest campaign mechanics with selected high-response demographic groups.
3. Build bundles around the top product categories for the selected audience, then measure incremental conversion against a control group.
4. Use the response-by-country view to localise offers only after checking each market has a sufficient customer base.
5. Test a targeted web incentive or checkout simplification for high-visit, low-spend non-responders—the defined underserved group.
6. Compare web, store, and catalogue activity by response before choosing a delivery channel; do not infer causation from the observed association.

## 6. Dashboard guide

Run `streamlit run app.py`. Use Country, Education, Marital Status, Age Band, Income Band, and latest-campaign-outcome filters in the sidebar. The dashboard has five views: executive overview, campaign performance, customer behaviour, targeting, and a downloadable data explorer. All metrics and visuals recompute from the selected audience.

## 7. Reproducibility

1. Install dependencies from `requirements.txt` (and Plotly if it is not already installed).
2. Run `python src/data_cleaning.py` when the raw input files are available.
3. Run `python src/segmentation.py`, `python src/eda.py`, and `python src/business_analysis.py`.
4. Run `python sql/load_data.py`, then `python src/run_sql.py`.
5. Start the dashboard with `streamlit run app.py`.

## 8. Limitations

The data supports exploratory, historical analysis only. It does not identify campaign costs, profit, experiment assignment, or causal treatment effects. Future work should retain campaign costs and use controlled experiments to estimate incremental lift and ROI.
