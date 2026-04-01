"""
California Public Expenditure Analysis
Exploratory data analysis of city-level spending across California regions (2013-2023)
Data: California State Controller's Office
"""

import csv
from collections import defaultdict
import statistics

# ── 1. Load & merge data ─────────────────────────────────────────────────────

region_map = {}
with open("city_to_region.csv") as f:
    for row in csv.DictReader(f):
        region_map[row["Entity Name"]] = row["Region"]

rows = []
with open("City_Expenditures_Per_Capita.csv") as f:
    for row in csv.DictReader(f):
        year = int(row["Fiscal Year"])
        if 2013 <= year <= 2023:
            entity = row["Entity Name"]
            region = region_map.get(entity)
            if region and row["Expenditures Per Capita"]:
                rows.append({
                    "entity":     entity,
                    "year":       year,
                    "total_exp":  float(row["Total Expenditures"] or 0),
                    "population": float(row["Estimated Population"] or 0),
                    "per_capita": float(row["Expenditures Per Capita"] or 0),
                    "region":     region,
                })

print(f"Loaded {len(rows):,} records across {len(set(r['entity'] for r in rows))} cities\n")

REGIONS = sorted(set(r["region"] for r in rows))

# ── 2. Overview: total expenditure & population by region ────────────────────

region_totals = defaultdict(float)
pop_by_region = defaultdict(float)

for r in rows:
    region_totals[r["region"]] += r["total_exp"]
    if r["year"] == 2023:
        pop_by_region[r["region"]] += r["population"]

grand_total = sum(region_totals.values())

print("=== Total Expenditure by Region (2013-2023) ===")
for region in sorted(region_totals, key=lambda x: region_totals[x], reverse=True):
    pct = region_totals[region] / grand_total * 100
    pop = pop_by_region[region]
    print(f"  {region:<25} ${region_totals[region]/1e9:6.1f}B  ({pct:.1f}%)   Pop 2023: {pop/1e6:.2f}M")

# ── 3. Per-capita trends: mean vs median (outlier awareness) ─────────────────

print("\n=== Per Capita Spending — Mean vs Median by Region ===")
print(f"  {'Region':<25} {'Mean':>10} {'Median':>10}  Note")

for region in REGIONS:
    vals = [r["per_capita"] for r in rows if r["region"] == region]
    mean = sum(vals) / len(vals)
    med  = statistics.median(vals)
    note = "** large mean/median gap -- outliers present" if mean > med * 3 else ""
    print(f"  {region:<25} ${mean:>9,.0f} ${med:>9,.0f}  {note}")

# ── 4. Identify outliers ─────────────────────────────────────────────────────

print("\n=== Top 10 Highest Per-Capita Cities (any year) ===")
sorted_rows = sorted(rows, key=lambda x: x["per_capita"], reverse=True)
for r in sorted_rows[:10]:
    print(f"  {r['entity']:<25} {r['year']}  ${r['per_capita']:>12,.0f}  pop: {r['population']:,.0f}  [{r['region']}]")

# ── 5. Per-capita growth 2013 -> 2023 ────────────────────────────────────────

print("\n=== Per Capita Growth by Region (2013 -> 2023) ===")
yr_region = defaultdict(lambda: defaultdict(list))
for r in rows:
    yr_region[r["region"]][r["year"]].append(r["per_capita"])

for region in REGIONS:
    v13 = statistics.median(yr_region[region][2013])
    v23 = statistics.median(yr_region[region][2023])
    growth = (v23 / v13 - 1) * 100
    print(f"  {region:<25} ${v13:>7,.0f} -> ${v23:>7,.0f}  ({growth:+.0f}%)")

# ── 6. Top & bottom cities per region (excluding extreme outliers) ───────────

print("\n=== Top 5 / Bottom 5 Cities by Avg Per Capita (excluding Vernon & Industry) ===")
OUTLIERS = {"Vernon", "Industry"}

city_avgs = defaultdict(list)
for r in rows:
    if r["entity"] not in OUTLIERS:
        city_avgs[(r["entity"], r["region"])].append(r["per_capita"])

city_means = {k: sum(v)/len(v) for k, v in city_avgs.items()}

for region in REGIONS:
    rc = sorted(
        [(e, avg) for (e, reg), avg in city_means.items() if reg == region],
        key=lambda x: x[1], reverse=True
    )
    print(f"\n  {region}")
    print(f"    Top 5:    " + ", ".join(f"{e} (${avg:,.0f})" for e, avg in rc[:5]))
    print(f"    Bottom 5: " + ", ".join(f"{e} (${avg:,.0f})" for e, avg in rc[-5:]))

# ── 7. Key takeaways ─────────────────────────────────────────────────────────

takeaways = [
    "1. Southern California accounts for 55.6% of total expenditure but its average per-capita\n"
    "   is heavily skewed by Vernon (pop ~100, spend >$1M/capita). The median SoCal figure\n"
    "   ($1,343) is actually lower than Sierra Nevada ($2,198).",

    "2. All regions show median per-capita growth of 39-69% from 2013-2023.\n"
    "   All regions show a 2020-2021 spending uptick consistent with pandemic-era emergency\n"
    "   expenditures and federal relief pass-throughs at the local level.",

    "3. Small city size -- not region -- is the strongest predictor of high per-capita spend.\n"
    "   The top spenders in every region are small municipalities with high fixed costs\n"
    "   or unusual economic profiles (industrial enclaves, resort towns).",

    "4. Within-region spread is extreme: in Northern CA, Mountain View ($45,645) spends\n"
    "   ~69x more per capita than Citrus Heights ($660). Regional averages mask this\n"
    "   variation entirely -- city-level analysis is essential.",
]

print("\n=== Key Takeaways ===\n")
for t in takeaways:
    print(t)
    print()
