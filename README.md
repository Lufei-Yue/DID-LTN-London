# How Effective are Low Traffic Neighbourhoods in Reducing Traffic Accidents? A City-Wide Difference-in-differences Study in London

## Overview 

Low Traffic Neighbourhoods (LTNs) are urban planning interventions aimed at reducing through traffic and improving road safety for pedestrians and cyclists. This study evaluates the effectiveness of LTNs in reducing traffic accidents in London using a Difference-in-Differences (DID) approach. The study analyzes annual traffic accident data from 2015 to mid 2024 and employs both a traditional DID model and an improved DID model to assess the short- and long-term effects of LTNs. I am currently preparing for publication.


## Data Preparation 

### Data

•	LTNs (update to August 2024): https://blog.westminster.ac.uk/ata/projects/london-ltn-dataset/
                                https://www.healthystreetsscorecard.london/ltn-low-traffic-neighbourhood-schemes-mapping/

•	London borough: https://data.london.gov.uk/dataset/london_boroughs

•	STAT19 (Road Safety Data): py-stats19 - https://pypi.org/project/pystats19/


### Data preprocessing
•	Selected the timeframe. Evaluation of eligible LTN areas implemented between 1 January 2020 and 1 January 2022 and in place until August 2024. 

•	Accident data were spatially joined to areas inside or outside the LTN areas in each borough, and the annual number was also aggregated separately. As the 2024 collisions data is only updated up to June, the number of accidents in 2024 with each borough inside and outside the LTN is processed by multiplying the half-yearly values by two.

•	In calculating the annual number of accidents outside the LTN areas in each borough, the areas in each borough containing LTNs introduced before 1 January 2020 were also removed, with the accidents in the remaining areas forming a **control group**. This is because we need to ensure that the control group always represents areas that are not affected by LTNs.

•	For the eligible LTN areas, we selected the LTNs that were implemented between 1 January 2020 and 1 January 2022, and would not be removed until August 2024, as the **treatment group**. The annual number of accidents in these eligible LTN areas was calculated for each borough (include a 10 meter buffer).

•	Removed boroughs - outliers (City of London) and with low number of accidents in LTNs (the average of less than 5 from 2015 to 2024).  


<img width="5429" height="3829" alt="featured" src="https://github.com/user-attachments/assets/deee969e-9c3c-4b23-be7f-5c04e49cbd05" />


**Figure 1**. Map of London boroughs and related LTNs.

<img width="1389" height="458" alt="image" src="https://github.com/user-attachments/assets/96033410-c943-4e07-a845-7ff560cedcec" />


**Figure 2.** Timeline of LTNs Implementation and Removal.

## Methodology

### Traditional Difference-in-Differences (DID) Analysis

Quantify the impact of LTNs on traffic accidents.

![image](https://github.com/user-attachments/assets/53d6ae49-b43d-474a-b895-cb2b2ef028d1)

•	Y<sub>it</sub>: Logged annual accident count for the area in borough i in a given year t.

•	treatment<sub>i</sub>: A binary variable indicating whether the area i in a borough is a LTN (1) or not (0).

•	post<sub>t</sub>: A binary variable indicating the period; the year t before the implementation of LTNs (before 2020) is 0, and the year t after the implementation of LTNs (after 2020) is 1.

•	treatment<sub>i</sub> × post<sub>t</sub>: An interaction term indicating the effect of LTNs on treated boroughs after their implementation. This is the key coefficient of interest.

•	ε: Error term.

<img width="977" height="518" alt="image" src="https://github.com/user-attachments/assets/4785eb88-ea44-4f5d-ba29-4b71e4d793f7" />

**Figure 3.** Conceptual illustration of the classic DID model.


### Improved   Difference-in-Differences (DID) Analysis

The Difference-in-Differences (DID) method is a widely used quasi-experimental technique for estimating causal relationships by comparing the differences in outcomes over time between a treatment group and a control group. The DID approach helps to eliminate biases that could arise from permanent differences between the groups and from time trends unrelated to the treatment. In this study, the DID method is employed to evaluate the impact of Low Traffic Neighbourhoods (LTNs) on the annual number of traffic accidents in London boroughs.

By using the traditional DID model, we have only captured the immediate effect of LTNs on accidents. There is also some unobserved heterogeneity and time-varying effects. To  account for unobserved heterogeneity, time-varying effects, and long-term effects of LTNs on road safety, an improved DID model was employed. 

The addition of time trend terms (timebefore_t and timeafter_t ) is to capture the overall trend in road safety over time before and after the implementation of the LTN policy, so that we can identify whether the LTNs have a better safety record. This helps to distinguish the effects of the LTN policy from general changes in the level of road safety in the city as a whole. 

To add the interactive items with the treatment group(treatment_i * timebefore_t and treatment_i * timeafter_t), which can quantify the impact of the LTN policy on road safety changes over time.

Model Specification:

![image](https://github.com/user-attachments/assets/076525ab-a555-43e4-bedc-d5e69d9888c8)

•	timebefore<sub>t</sub>: Number of years since the start of the observation period.

•	timeafter<sub>t</sub>: Number of years since the start of the treatment.

•	treatment<sub>i</sub> × timebefore<sub>t</sub>: Represents the difference in the trend in the number of accidents between the treatment and control groups before the introduction of LTNs. The effect of accident counts before the implementation of LTNs, allowing for the assessment of parallel trends assumption.

•	treatment<sub>i</sub> × timeafter<sub>t</sub>: The gradual change of accident counts in LTN areas after the LTNs have been introduced.

In this model, we have removed the data from 2020 to 2021 as all eligible LTNs were introduced during this period and we were able to avoid the impact of the pandemic.

<img width="927" height="560" alt="image" src="https://github.com/user-attachments/assets/7c4d90e0-928e-4705-b9e6-e003aee00dab" />

**Figure 4.** Conceptual illustration of the improved DID model.


## Results  

### Comparison of Traffic Accident inside and outside LTNs

<img width="865" height="445" alt="image" src="https://github.com/user-attachments/assets/f8bbe209-2d5b-4569-8f7e-d877c40b1400" />

**Figure 5.** Annual accident counts of inside and outside LTNs in the Greater London from 2015 to 2024.


Figure 5 presents the aggregate annual number of traffic cashes inside and outside the eligible LTNs. Before the implementation of eligible LTNs, both areas show similar trends. However, after the implementation of LTNs in 2020, the number of crashes in LTNs continues to decline, whereas the overall city accident counts increase post-pandemic. 

<img width="865" height="508" alt="image" src="https://github.com/user-attachments/assets/617714f7-8d83-4792-820d-9edcd84e5616" />

**Figure 6.** The absolute change and percentage trend compared between inside and outside LTNs in each borough before (2015-2019) and after (2020-2024) the implementation of LTNs.

Figure 6 further compares the annual average number of crashes inside and outside eligible LTNs within each borough, before and after the implantation. It shows the absolute and percentage change for London as a whole. The blue bars represent the change inside eligible LTNs, and the orange bars represent the change outside eligible LTNs. This figure highlights considerable variation between boroughs. Most LTNs show a reduction in the number of crashes and the boroughs with an increased change in LTNs tend to have a low number of crashes, for example, Enfield, have a low annual number of crashes on LTNs (1/3 of the average).


### Traditional DID Analysis on Traffic Accidents

**Table 1**. Basic DID model result.

<img width="1014" height="453" alt="image" src="https://github.com/user-attachments/assets/10d6df24-b789-40d6-ae17-d658dd17a7cc" />

•	Table 1 indicates the implementation of LTNs resulted in a 0.3072 reduction in the logged value of traffic accidents.

•	The traditional DID indicated the immediate reduction in accident counts after LTNs implementation.  

### Improved DID Analysis on Traffic Accidents

**Table 2.** Improved DID model result.

<img width="999" height="441" alt="image" src="https://github.com/user-attachments/assets/15be878a-41ce-48c2-bd9e-870c22d0fd54" />

•	Table 2 shows that in the long term (after the introduction of LTN in 2020 and continuing until 2024), LTNs significantly reduced road accidents, with an estimated reduction of 0.2404 in the logged value of annual road accidents.

•	The parallel trend assumption is critical to the internal validity of a DID model. It assumes that in the absence of treatment, the difference between the treatment and control groups would remain constant over time. To determine whether the model satisfied the parallel trend assumption, the interaction term treatment_i * timebefore_t must not be significant. Table 2 shows that the interaction term treatment_i * timebefore_t is not significant, which means that the parallel trends assumption is met.

•	The improved model separated short-term and long-term effects, providing a deeper understanding of the impact of LTNs on road safety.

•	This sustained reduction highlights the sustainable contribution of LTNs to a safer urban environment.


## Installation  

Ensure you have Python installed, then install required dependencies using:  

pip install pystats19 pandas geopandas numpy statsmodels matplotlib scipy
