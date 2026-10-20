# Winning the Space Race with Data Science — IBM Data Science Capstone

**Author:** Marcos Roque Rosa · **Course:** IBM Data Science Professional Certificate — Applied Data Science Capstone

SpaceX advertises Falcon 9 launches at about $62 million, against $165 million+ for other providers, largely because the first stage can be landed and reused. This project predicts whether a Falcon 9 first stage will land, so a competitor ("Space Y") can estimate the cost of a launch.

📄 **Final presentation:** [PDF](presentation/Marcos_Roque_Rosa_SpaceX_Capstone.pdf) · [PowerPoint](presentation/Marcos_Roque_Rosa_SpaceX_Capstone.pptx)

## Key results

| | |
|---|---|
| Data | 90 Falcon 9 launches (2010 – Nov 2020), 66.7 % first-stage landing success |
| Trend | 0 % landings before 2014 → 84–90 % in 2019–2020 |
| Best site | KSC LC-39A — 76.9 % success, 41.7 % of all successful landings |
| Orbits | SSO, VLEO and LEO land most often; GTO is hardest (52 %) |
| Models | Logistic Regression, SVM, Decision Tree and KNN all reach 83.3 % test accuracy; the **Decision Tree** has the best cross-validation accuracy (87.7 %) |

## Notebooks and app

| # | File | Lab |
|---|------|-----|
| 1 | [jupyter-labs-spacex-data-collection-api-v2.ipynb](jupyter-labs-spacex-data-collection-api-v2.ipynb) | Data collection with the SpaceX REST API |
| 2 | [jupyter-labs-webscraping.ipynb](jupyter-labs-webscraping.ipynb) | Web scraping Falcon 9 launch records from Wikipedia |
| 3 | [labs-jupyter-spacex-Data wrangling-v2.ipynb](labs-jupyter-spacex-Data%20wrangling-v2.ipynb) | Data wrangling and landing labels |
| 4 | [jupyter-labs-eda-sql-coursera_sqllite.ipynb](jupyter-labs-eda-sql-coursera_sqllite.ipynb) | EDA with SQL (SQLite) |
| 5 | [jupyter-labs-eda-dataviz-v2.ipynb](jupyter-labs-eda-dataviz-v2.ipynb) | EDA with visualization and feature engineering |
| 6 | [lab-jupyter-launch-site-location-v2.ipynb](lab-jupyter-launch-site-location-v2.ipynb) | Interactive launch-site analysis with Folium |
| 7 | [spacex_dash_app.py](spacex_dash_app.py) | Plotly Dash dashboard (uses [spacex_launch_dash.csv](spacex_launch_dash.csv)) |
| 8 | [SpaceX-Machine-Learning-Prediction-Part-5-v1.ipynb](SpaceX-Machine-Learning-Prediction-Part-5-v1.ipynb) | Machine-learning prediction |

Other folders: [`data/`](data) — datasets produced by the notebooks · [`maps/`](maps) — saved Folium maps (open in a browser) · [`images/`](images) — dashboard and map screenshots used in the presentation.

### Run the dashboard

```bash
python -m pip install pandas dash
python spacex_dash_app.py      # then open http://127.0.0.1:8050
```

## Execution notes

* The public SpaceX API (`api.spacexdata.com`) was offline (HTTP 522) when the notebooks were run in October 2026. The API notebook's code is unchanged and works against the live API; for this run its requests were answered from IBM's archived copies of the same API responses, and its output reproduces IBM's reference `dataset_part_1.csv` exactly.
* scikit-learn 1.3+ removed `max_features='auto'`; the Decision Tree grid uses `'sqrt'` and `'log2'`.
* Newer Folium no longer ships the Glyphicons font, so launch markers use a Font Awesome rocket icon on a green/red marker.

Map tiles © OpenStreetMap contributors.
