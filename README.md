# How Effective are Low Traffic Neighbourhoods in Reducing Traffic Accidents? A City-Wide Difference-in-differences Study in London

## Overview 

Low Traffic Neighbourhoods (LTNs) are urban planning interventions aimed at reducing through traffic and improving road safety for pedestrians and cyclists. This study evaluates the effectiveness of LTNs in reducing traffic accidents in London using a Difference-in-Differences (DID) approach. The study analyzes annual traffic accident data from 2015 to mid 2024 and employs both a traditional DID model and an improved DID model to assess the short- and long-term effects of LTNs.  


## Data Preparation 

### Data

•	Low Traffic Neighbourhood (LTN) areas (update to August 2024)

•	London borough

•	STAT19 (Road Safety Data): Extracted collisions data from 2015 to mid-2024 (30 June 2024).

### Data preprocessing
•	Selected the timeframe. Evaluation of eligible LTN areas implemented between 1 January 2020 and 1 January 2022 and in place until August 2024. 

•	Accident data were spatially joined to areas inside or outside the LTN areas in each borough, and the annual number was also aggregated separately. As the 2024 collisions data is only updated up to June, the number of accidents in 2024 with each borough inside and outside the LTN is processed by multiplying the half-yearly values by two.

•	In calculating the annual number of accidents outside the LTN areas in each borough, the areas in each borough containing LTNs introduced before 1 January 2020 were also removed, with the accidents in the remaining areas forming a **control group**. This is because we need to ensure that the control group always represents areas that are not affected by LTNs.

•	For the eligible LTN areas, we selected the LTNs that were implemented between 1 January 2020 and 1 January 2022, and would not be removed until August 2024, as the **treatment group**. The annual number of accidents in these eligible LTN areas was calculated for each borough (include a 10 meter buffer).

•	Removed boroughs - outliers (City of London) and with low number of accidents in LTNs (the average of less than 5 from 2015 to 2024).  


![image](https://github.com/user-attachments/assets/da15ec6b-a50f-4905-9803-61a38818461a)

**Figure 1**. Map of London boroughs and related LTNs.

![image](https://github.com/user-attachments/assets/8abd2022-d2b1-4726-8c00-6c1f7359c5b3)

**Figure 2.** Timeline of LTNs Implementation and Removal.

## Methodology

### Traditional Difference-in-Differences (DID) Analysis

Quantify the impact of LTNs on traffic accidents.

![image](https://github.com/user-attachments/assets/53d6ae49-b43d-474a-b895-cb2b2ef028d1)

•	Y_it: logged annual accident count for the area in a borough i in a given year t.

•	treatment_i: a binary variable indicates whether the area i in a borough is a LTN (1) or not (0).

•	post_t: a binary variable indicates the period, the year t before the implementation of LTNs (before 2020) is 0, and the year t after the implementation of LTNs (after 2020) is 1.

•	treatment_i * post_t: an interaction term indicating the effect of LTNs on treated boroughs after their implementation. This is the key coefficient of interest.

•	ε: Error term.

### Improved   Difference-in-Differences (DID) Analysis

The Difference-in-Differences (DID) method is a widely used quasi-experimental technique for estimating causal relationships by comparing the differences in outcomes over time between a treatment group and a control group. The DID approach helps to eliminate biases that could arise from permanent differences between the groups and from time trends unrelated to the treatment. In this study, the DID method is employed to evaluate the impact of Low Traffic Neighbourhoods (LTNs) on the annual number of traffic accidents in London boroughs.

By using the traditional DID model, we have only captured the immediate effect of LTNs on accidents. There is also some unobserved heterogeneity and time-varying effects. To  account for unobserved heterogeneity, time-varying effects, and long-term effects of LTNs on road safety, an improved DID model was employed. 

The addition of time trend terms (timebefore_t and timeafter_t ) is to capture the overall trend in road safety over time before and after the implementation of the LTN policy, so that we can identify whether the LTNs have a better safety record. This helps to distinguish the effects of the LTN policy from general changes in the level of road safety in the city as a whole. 

To add the interactive items with the treatment group(treatment_i * timebefore_t and treatment_i * timeafter_t), which can quantify the impact of the LTN policy on road safety changes over time.

Model Specification:

![image](https://github.com/user-attachments/assets/076525ab-a555-43e4-bedc-d5e69d9888c8)

•	timebefore_t : Number of years since the start of the observation period.

•	timeafter_t: Number of years since the start of the treatment.

•	treatment_i * timebefore_t: Represents the difference in the trend in the number of accidents between the treatment and control groups before the introduction of LTNs, The effect of accident counts before the implementation of LTNs, allowing for the assessment of parallel trends assumption.

•	treatment_i * timeafter_t: The gradual change of accident counts in LTN areas when after the LTNs have been introduced.

In this model, we have removed the data from 2020 to 2021 as all eligible LTNs were introduced during this period and we were able to avoid the impact of the pandemic.


## Results  

### Comparison of Traffic Accident inside and outside LTNs

![image](https://github.com/user-attachments/assets/da7cfab1-0cb7-43a6-b47e-3b745fcb09d3)

**Figure 3.** Accident counts of inside and outside LTNs in each borough from 2015 to 2024.


Figure 3 shows that after the introduction of LTNs in 2020, the number of accidents within LTNs decreased, while the number of accidents in the city as a whole increased in the post-pandemic period.


![image](https://github.com/user-attachments/assets/738b913d-4f4b-4412-b0ea-acd571b7bfce)


**Figure 4.** The absolute change and percentage trend inside and outside LTNs in each borough.

Figure 4 shows the absolute and percentage change for London as a whole. The orange shows the change in all boroughs and the blue shows the change in eligible LTNs in each borough. Most LTNs show a reduction in the number of accidents and the boroughs with an increased change in LTNs tend to have a low number of accidents, for example, Enfield, have a low annual number of accidents on LTNs (1/3 of the average).


### Traditional DID Analysis on Traffic Accidents

**Table 1**. Basic DID model result.

![image](https://github.com/user-attachments/assets/1766f346-4793-4a80-8f6a-08d665452ec8)

•	Table 1 indicates the implementation of LTNs resulted in a 0.3072 reduction in the logged value of traffic accidents.

•	The traditional DID indicated the immediate reduction in accident counts after LTNs implementation.  

### Improved DID Analysis on Traffic Accidents

**Table 2.** Improved DID model result.

![image](https://github.com/user-attachments/assets/2092f252-23f1-422b-ad5c-5a4aa85be82a)

•	Table 2 shows that in the long term (after the introduction of LTN in 2020 and continuing until 2024), LTNs significantly reduced road accidents, with an estimated reduction of 0.1066 in the logged value of annual road accidents.

•	The parallel trend assumption is critical to the internal validity of a DID model. It assumes that in the absence of treatment, the difference between the treatment and control groups would remain constant over time. To determine whether the model satisfied the parallel trend assumption, the interaction term treatment_i * timebefore_t must not be significant. Table 2 shows that the interaction term treatment_i * timebefore_t is not significant, which means that the parallel trends assumption is met.

•	The improved model separated short-term and long-term effects, providing a deeper understanding of the impact of LTNs on road safety.

•	This sustained reduction highlights the sustainable contribution of LTNs to a safer urban environment.


## Installation  

Ensure you have Python installed, then install required dependencies using:  

pip install pystats19 pandas geopandas numpy statsmodels matplotlib scipy


## References  

py-stats19

London LTN dataset: https://blog.westminster.ac.uk/ata/projects/london-ltn-dataset/

https://www.healthystreetsscorecard.london/ltn-low-traffic-neighbourhood-schemes-mapping/

London boundary: https://data.london.gov.uk/dataset/london_boroughs
