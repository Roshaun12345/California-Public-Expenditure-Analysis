# California Public Expenditure Analysis

An interactive data visualization and analysis of public spending across California's four regions — Northern California, Southern California, Central California, and Sierra Nevada — from 2013 to 2023.

**Live site:** https://roshaun12345.github.io/California-Public-Expenditure-Analysis/  
**Analysis notebook:** https://roshaun12345.github.io/California-Public-Expenditure-Analysis/analysis.html

---

## Key Findings

- **Southern California's average is misleading.** Vernon, an industrial city of ~100 residents, spends over $2M per capita, pushing the regional mean to $11,762 against a median of just $1,343 (a ratio of 8.8x). Median is the right metric.
- **Northern California grew the fastest.** Median per-capita spending rose 69% from 2013 to 2023, driven by Bay Area cities like Mountain View and San Francisco.
- **City size predicts spending more than region.** The top spenders in every region are small municipalities, resort towns, tech enclaves, coastal cities, with high fixed costs relative to their populations.
- **Within-region variation is extreme.** In Northern California alone, Mountain View ($45,645) spends 69x more per capita than Citrus Heights ($660).

---

## Visualizations

| Chart | Description |
|---|---|
| Multi-Line Chart | Regional population trends 2013-2023 |
| Pie Chart | Total expenditure share by region |
| Heatmap | Per-capita expenditure by region and year |
| Small Multiples | Top 5 and bottom 5 cities per region |
| Scatter Plot | City-level spending vs. population |

---

## Stack

- **D3.js v7** — all visualizations built from scratch
- **Python / pandas** — exploratory data analysis
- **Jupyter Notebook** — analysis workflow
- **GitHub Pages** — hosting

---

## Data

- `City_Expenditures_Per_Capita.csv` — city-level expenditure and population data from the California State Controller's Office
- `city_to_region.csv` — mapping of cities to California regions

---

## Author

Roshaun Gregory
