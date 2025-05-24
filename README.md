# Air Quality Analysis
This project analyzes air quality data across various Indian states using pollutant-level measurements. It includes data preprocessing, exploratory data analysis, and the creation of a "Breathability Risk Index" (BRI) to categorize the relative air pollution risk per state. The insights can aid public health understanding, policy making, and risk assessment for insurance or environmental planning.

## Project Structure
* aq_data_230525.csv: Raw dataset containing air pollution levels and metadata.
* preprocessing.py: Script for cleaning and imputing missing values.
* EDA.py: Exploratory Data Analysis and BRI computation.
* map_visuals_bri.py: Generates an interactive map visualization for BRI across states.

## 🌫️ Pollutants
The dataset tracks concentrations of seven key air pollutants. Each pollutant affects health and the environment in distinct ways:

| Pollutant                   | Description                                                            | Sources                                                                               | Health Effects                                                                                    | Environmental Impact                                                                  |
| --------------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| **PM2.5**                   | Fine particulate matter with diameter ≤ 2.5 microns                    | Combustion engines, industrial emissions, residential burning (wood, coal), wildfires | Penetrates deep into lungs and bloodstream; causes respiratory and cardiovascular issues, cancer  | Reduces visibility (smog), affects climate by altering solar radiation                |
| **PM10**                    | Coarse particulate matter with diameter ≤ 10 microns                   | Road dust, construction activities, mining, agriculture                               | Irritates eyes, nose, throat; worsens asthma and bronchitis                                       | Dust deposition on plants and buildings, visibility reduction                         |
| **NO₂ (Nitrogen Dioxide)**  | A reddish-brown gas with strong odor                                   | Motor vehicles, power plants, industrial processes                                    | Causes inflammation of the airways, decreases lung function, increases asthma risk                | Contributes to smog and acid rain, harms vegetation                                   |
| **SO₂ (Sulfur Dioxide)**    | A colorless gas with pungent smell                                     | Coal and oil combustion, smelting metal ores                                          | Triggers asthma, bronchitis, and lung inflammation                                                | Precursor to acid rain, damages crops and aquatic ecosystems                          |
| **CO (Carbon Monoxide)**    | Colorless, odorless gas                                                | Incomplete combustion of fossil fuels (vehicles, generators, heating systems)         | Binds with hemoglobin, reducing oxygen supply to organs; especially dangerous for heart and brain | Contributes indirectly to ground-level ozone formation                                |
| **O₃ (Ground-level Ozone)** | Not emitted directly; formed by reaction of sunlight with NOx and VOCs | Photochemical reactions involving traffic and industrial emissions                    | Causes throat irritation, coughing, chest pain, lung inflammation                                 | Damages crops, rubber, and building materials                                         |
| **NH₃ (Ammonia)**           | Colorless gas with a pungent smell                                     | Agricultural activities (fertilizer use, livestock waste), industrial processes       | Causes eye, nose, and throat irritation; long-term exposure can damage lungs                      | Contributes to particulate matter formation (e.g., ammonium nitrate), leading to haze |



## 🧹 Data Preprocessing
Steps taken in preprocessing.py:
1. Column Cleanup: Removed the country column (only one country present).
2. Date Formatting: Converted last_update to datetime.
3. Missing Values Handling:
  * Used pollutant-specific averages to impute missing values for pollutant_min, pollutant_max, and pollutant_avg.
  * Missing values were not dropped to preserve geographic and temporal diversity in the data.
4. Export: Cleaned data saved to aq_data_230525_cleaned.csv.


## 📊 Data Analysis
Performed using EDA.py:
* Descriptive Statistics: Examined distributions, means, and medians for pollutants.
* Visualizations:
  * Histograms for each pollutant showing mean vs. median.
  * Box plots grouped by pollutant_id.
* Breathability Risk Index (BRI):
  * Weighted scoring based on pollutant concentration using the following weights:
      * PM2.5: 0.30
      * PM10: 0.20
      * NO2: 0.15
      * SO2: 0.10
      * CO: 0.10
      * OZONE: 0.10
      * NH3: 0.05
* Normalized and scaled BRI scores (0–10).
* Categorized into:
  * Low Risk: BRI < 3
  * Moderate Risk: 3 ≤ BRI < 6
  * High Risk: BRI ≥ 6
* State-wise Pollutant Analysis: Bar plots of pollutant levels by state and associated BRI categories.

## 🗺️ Visualization

Generated via map_visuals_bri.py:
  * Interactive Folium map showing:
    * State-wise BRI
    * Risk categories via color-coded markers:
      
      🟢 Low Risk
      🟠 Moderate Risk
      🔴 High Risk

## 🧠 Conclusion & Insights

* PM2.5 and PM10 are the most influential pollutants in determining air quality risk.
* Urban and industrialized states generally showed higher BRI scores, indicating more polluted air.
* States with lower pollution risk may benefit from preventive regulation, while high-risk regions require immediate mitigation strategies.
* The BRI metric simplifies communication of air quality health risk and can be used by stakeholders like:
  * Public health agencies
  * Environmental bodies
  * Insurance companies
