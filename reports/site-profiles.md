# Site profiles

Twelve regions, ten selected on recurring global flood impact and two in the UAE.
Rainfall is the peak 24-hour depth at the named station, converted from the stored
millimetre value. Affected area is inundated extent, not the administrative area of
the affected districts, except where the method column says otherwise.

Evidence tiers: **V1** satellite-derived extent or official gauge record; **V2** government or UN agency report; **V3** reputable secondary reporting; **I** inferred, requires an explanatory note.

## Mumbai, India

`ind_mumbai` · bbox 72.775, 18.89, 72.98, 19.27 (EPSG:4326)

**Mechanism.** urban pluvial flooding locked in by high tide, which stops the drains and the Mithi discharging

**Why it is here.** Drainage sized for about 25 mm/hr against monsoon bursts many times that, in a city of twelve million ([source](https://questionofcities.org/mithi-more-than-a-rainwater-drain-for-mumbai-but-tell-that-to-the-authorities/))

**Where it floods first.** Hindmata (Dadar/Parel); Kurla; Sion; Matunga; King's Circle; Andheri and Vile Parle subways; Chembur; Vikhroli

**Exposure.** [12,442,373 people](https://en.wikipedia.org/wiki/Mumbai) over a 603 km² catchment.

| Event | Dates | Peak 24h rain (cm) | Event total (cm) | Station | Inundated area (km²) | Area method | Driver | Deaths |
|---|---|---|---|---|---|---|---|---|
| ind_mumbai_2005 | 2005-07-26 to 2005-07-27 | [94.4](https://en.wikipedia.org/wiki/Maharashtra_floods_of_2005) `V3` |  | Santacruz (IMD) | not published |  | rainfall | 1,094 |
| ind_mumbai_2017 | 2017-08-29 to 2017-08-30 | [32.2](https://en.wikipedia.org/wiki/2017_Mumbai_flood) `V3` |  | Santacruz (IMD) | not published |  | rainfall | 21 |
| ind_mumbai_2019 | 2019-07-01 to 2019-07-02 | [30.0](https://www.aljazeera.com/gallery/2019/7/2/in-pictures-india-monsoon-chaos-kills-dozens-in-mumbai-pune) `V3` |  | unspecified Mumbai station | not published |  | rainfall | 27 |
| ind_mumbai_2021 | 2021-07-17 to 2021-07-19 | [23.5](https://floodlist.com/asia/india-mumbai-landslides-july-2021) `V3` |  | Mumbai Airport (Santacruz) | not published |  | rainfall | 32 |
| ind_mumbai_2024 | 2024-09-27 to 2024-09-28 |  | [25.0](https://watchers.news/2024/09/28/mumbai-sees-its-wettest-september-day-in-3-years-after-250-mm-9-8-inches-of-rain-hit-the-city-in-6-hours-india/) `V3` |  | not published |  | rainfall | 4 |

## Jakarta, Indonesia

`idn_jakarta` · bbox 106.68, -6.37, 106.97, -6.08 (EPSG:4326)

**Mechanism.** urban pluvial flooding on a coastal plain that is sinking faster than the drainage can be rebuilt

**Why it is here.** Around 240 square kilometres of the city already sits below sea level and subsidence reaches 17.5 cm a year, so gravity drainage into the Ciliwung keeps failing ([source](https://www.sciencedirect.com/science/article/pii/S2590252023000053))

**Where it floods first.** Kampung Melayu; Kampung Pulo; Bidara Cina; Cipinang Melayu, all riverside kampungs on the Ciliwung

**Exposure.** [11,010,514 people](https://en.wikipedia.org/wiki/Jakarta) over a 662 km² catchment.

| Event | Dates | Peak 24h rain (cm) | Event total (cm) | Station | Inundated area (km²) | Area method | Driver | Deaths |
|---|---|---|---|---|---|---|---|---|
| idn_jakarta_2007 | 2007-02-01 to 2007-02-12 | [34.0](https://en.wikipedia.org/wiki/2007_Jakarta_flood) `V3` |  | unspecified (city-wide peak) | not published |  | rainfall | 80 |
| idn_jakarta_2013 | 2013-01-15 to 2013-01-23 |  |  |  | not published |  | levee_failure | 41 |
| idn_jakarta_2015 | 2015-02-01 to 2015-02-28 |  |  |  | not published |  | rainfall |  |
| idn_jakarta_2020 | 2020-01-01 to 2020-01-02 | [37.7](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2022GL101513) `V1` |  | Halim Perdanakusuma (BMKG) | not published |  | rainfall | 66 |
| idn_jakarta_2021 | 2021-02-19 to 2021-02-22 | [21.4](https://floodlist.com/asia/indonesia-greater-jakarta-floods-update-february-2021) `V3` |  | Majalengka (BMKG) | not published |  | rainfall | 5 |

## Mekong delta, Vietnam

`vnm_mekong` · bbox 104.5, 8.5, 106.8, 11.0 (EPSG:4326)

**Mechanism.** seasonal riverine flood pulse spreading across the flattest terrain in Vietnam

**Why it is here.** Nineteen million people on a delta at sea level, though the flood pulse itself is shrinking as upstream dams cut reverse flow into the Tonle Sap by 56 percent ([source](https://hess.copernicus.org/articles/26/609/2022/))

**Where it floods first.** An Giang; Dong Thap; Long An provinces. No neighbourhood-level list published for this rural deltaic system

**Exposure.** [19,000,000 people](https://en.wikipedia.org/wiki/Mekong_Delta) over a 40,519 km² catchment.

| Event | Dates | Peak 24h rain (cm) | Event total (cm) | Station | Inundated area (km²) | Area method | Driver | Deaths |
|---|---|---|---|---|---|---|---|---|
| vnm_mekong_2000 | 2000-09-01 to 2000-10-31 |  |  |  | [37,420](https://www.researchgate.net/publication/274679640_The_Historical_Flood_in_2000_in_Mekong_River_Delta_Vietnam_A_Quantitative_Analysis_and_Simulation) | simulated inundation extent (ISIS 1D/2D hydraulic model calibrated to the 2000 event; covers ~96% of the Vietnamese Mekong Delta area) | rainfall | 407 |
| vnm_mekong_2011 | 2011-09-01 to 2011-12-31 |  |  |  | not published |  | rainfall | 85 |

## Niger-Benue confluence, Lokoja, Nigeria

`nga_lokoja` · bbox 6.6, 7.65, 6.95, 7.95 (EPSG:4326)

**Mechanism.** riverine flooding at the confluence of Nigeria's two largest rivers, compounded by upstream dam releases

**Why it is here.** Downstream of Kainji and Jebba on the Niger and of Cameroon's Lagdo dam on the Benue, with no Nigerian counterpart reservoir to absorb the release ([source](https://www.environewsnigeria.com/30-years-of-nigerias-failure-to-tackle-cameroon-dam-flooding/))

**Where it floods first.** Lokoja town and the immediate confluence floodplain in Kogi State

**Exposure.** [791,000 people](https://www.macrotrends.net/global-metrics/cities/206383/lokoja/population) over a an unsourced catchment area catchment.

| Event | Dates | Peak 24h rain (cm) | Event total (cm) | Station | Inundated area (km²) | Area method | Driver | Deaths |
|---|---|---|---|---|---|---|---|---|
| nga_2012 | 2012-09-01 to 2012-11-30 |  |  |  | [60.6](https://www.researchgate.net/publication/273381186_Geospatial_Assessment_of_2012_Flood_Disaster_in_Kogi_State_Nigeria) | geospatial/remote-sensing assessment of inundated area, Niger-Benue confluence, Kogi State (academic paper abstract only; full text not independently verified) | rainfall+dam_release |  |
| nga_2018 | 2018-09-07 to 2018-09-24 |  |  |  | not published |  | rainfall+dam_release | 100 |
| nga_2022 | 2022-09-01 to 2022-10-10 |  |  |  | [154](https://user.eumetsat.int/resources/case-studies/severe-flooding-in-nigeria) | Sentinel-1 SAR flood delineation over Lokoja area, 25–26 Sep 2022 acquisition | rainfall+dam_release | 76 |
| nga_2024 | 2024-09-23 to 2024-11-01 |  |  |  | [610](https://reliefweb.int/report/nigeria/nigeria-floods-situation-report-no-5-1-november-2024) | government estimate of inundated farmland, Kogi State (OCHA situation report) | rainfall+dam_release |  |

## Houston, Harris County, United States

`usa_houston` · bbox -95.82, 29.49, -94.9, 30.17 (EPSG:4326)

**Mechanism.** pluvial and bayou flooding from stalled tropical systems over a flat, heavily paved coastal plain

**Why it is here.** Five federally declared flood disasters inside two decades on terrain with almost no drainage gradient ([source](https://en.wikipedia.org/wiki/Hurricane_Harvey))

**Where it floods first.** Buffalo Bayou; Brays Bayou; White Oak Bayou corridors across Harris County

**Exposure.** [5,009,302 people](https://en.wikipedia.org/wiki/Harris_County,_Texas) over a 4,603 km² catchment.

| Event | Dates | Peak 24h rain (cm) | Event total (cm) | Station | Inundated area (km²) | Area method | Driver | Deaths |
|---|---|---|---|---|---|---|---|---|
| usa_2001_allison | 2001-06-05 to 2001-06-09 |  | [94.0](https://www.cdc.gov/mmwr/preview/mmwrhtml/mm5117a1.htm) `V2` |  | not published |  | rainfall | 22 |
| usa_2015_memorial | 2015-05-25 to 2015-05-26 |  | [26.2](https://www.click2houston.com/weather/2019/05/23/remembering-houstons-2015-memorial-day-flood/) `V3` |  | not published |  | rainfall | 8 |
| usa_2016_taxday | 2016-04-17 to 2016-04-18 |  | [42.4](https://www.click2houston.com/weather/2019/04/16/look-back-at-houstons-2016-tax-day-flood/) `V3` |  | not published |  | rainfall | 5 |
| usa_2017_harvey | 2017-08-25 to 2017-08-31 |  | [153.9](https://www.nhc.noaa.gov/data/tcr/AL092017_Harvey.pdf) `V1` |  | [606](https://kinder.rice.edu/urbanedge/hurricane-harvey-data) | satellite imagery classification of flooded area, Harris County (University of Colorado analysis) | rainfall |  |
| usa_2024_beryl | 2024-07-08 to 2024-07-09 |  |  |  | not published |  | rainfall | 7 |

## Ahr valley and Rhine-Meuse, Germany and Belgium

`deu_ahr` · bbox 5.6, 49.9, 8.0, 51.05 (EPSG:4326)

**Mechanism.** flash flooding as slow-moving convective rain funnels down steep, narrow valley catchments

**Why it is here.** Copernicus's own historical flood record for Ahrweiler shows the valley floods repeatedly, and the 2021 event gave residents minutes rather than hours ([source](https://nhess.copernicus.org/articles/25/2007/2025/))

**Where it floods first.** Ahr valley (Ahrweiler, Bad Neuenahr, Schuld); Erft valley; Vesdre valley around Liege and Pepinster

**Exposure.** [250,200 people](https://en.wikipedia.org/wiki/Ahrweiler_(electoral_district)) over a 900 km² catchment.

| Event | Dates | Peak 24h rain (cm) | Event total (cm) | Station | Inundated area (km²) | Area method | Driver | Deaths |
|---|---|---|---|---|---|---|---|---|
| deu_2021_jul | 2021-07-12 to 2021-07-15 | [15.0](https://nhess.copernicus.org/articles/23/525/2023/) `V1` |  | Cologne-Stammheim | not published |  | rainfall | 134 |
| bel_2021_jul | 2021-07-13 to 2021-07-16 |  |  |  | not published |  | rainfall | 37 |

## Rio Grande do Sul, Porto Alegre, Brazil

`bra_rgs` · bbox -52.2, -30.35, -50.8, -29.3 (EPSG:4326)

**Mechanism.** riverine flooding where four rivers converge into Lake Guaiba and back water up into the city

**Why it is here.** Heavy rain anywhere across the Jacui, Taquari, Cai and Sinos basins converges on one city outlet, and attribution work ties the 2023 and 2024 extremes to El Nino plus warming ([source](https://en.wikipedia.org/wiki/2024_Rio_Grande_do_Sul_floods))

**Where it floods first.** Porto Alegre city centre and Sarandi; Canoas; the Taquari valley towns of Lajeado and Muçum

**Exposure.** [4,240,000 people](https://www.macrotrends.net/global-metrics/cities/20264/porto-alegre/population) over a 2,919 km² catchment.

| Event | Dates | Peak 24h rain (cm) | Event total (cm) | Station | Inundated area (km²) | Area method | Driver | Deaths |
|---|---|---|---|---|---|---|---|---|
| bra_2023_sep | 2023-09-01 to 2023-09-06 |  | [29.1](https://en.wikipedia.org/wiki/2023_Rio_Grande_do_Sul_floods) `V3` |  | not published |  | rainfall | 47 |
| bra_2024_apr_may | 2024-04-27 to 2024-05-12 |  |  |  | [1,557](https://www.sciencedirect.com/science/article/pii/S2666592125000411) | Sentinel-derived flood extent, cropland 1481 km2 and urban built-up 76.2 km2 summed | rainfall | 181 |

## Dubai and Sharjah, United Arab Emirates

`are_dubai` · bbox 54.85, 24.75, 55.65, 25.65 (EPSG:4326)

**Mechanism.** arid urban pluvial flooding where rare, very intense convective storms exceed what the drainage was ever sized for

**Why it is here.** The April 2024 storm was the heaviest since UAE records began in 1949, and the response was a 30 billion dirham drainage programme, which is what a structural shortfall looks like ([source](https://en.wikipedia.org/wiki/2024_United_Arab_Emirates_floods))

**Where it floods first.** Al Quoz and the D65 interchange; Nad Al Sheba; Sharjah city along King Abdulaziz Street

**Exposure.** [3,790,000 people](https://www.globalmediainsight.com/blog/dubai-population-statistics/) over a 4,110 km² catchment.

| Event | Dates | Peak 24h rain (cm) | Event total (cm) | Station | Inundated area (km²) | Area method | Driver | Deaths |
|---|---|---|---|---|---|---|---|---|
| dxb-2016-03 | 2016-03-09 to 2016-03-12 |  | [24.0](https://watchers.news/2016/03/09/severe-weather-hits-uae-and-oman-thunderstorms-large-hail-and-severe-flooding/) `V3` |  | not published |  | rainfall |  |
| dxb-2020-01 | 2020-01-09 to 2020-01-12 |  |  |  | not published |  | rainfall |  |
| dxb-2024-04 | 2024-04-14 to 2024-04-17 | [14.2](https://en.wikipedia.org/wiki/2024_United_Arab_Emirates_floods) `V3` | [16.4](https://en.wikipedia.org/wiki/2024_United_Arab_Emirates_floods) `V3` | Dubai International Airport | [23.8](https://www.tandfonline.com/doi/full/10.1080/19475683.2026.2639768) | satellite-derived flood extent — PlanetScope daily optical imagery (14–27 Apr 2024) classified with a U-Net deep-learning model | rainfall | 5 |
| dxb-2024-05 | 2024-05-02 to 2024-05-02 |  |  |  | not published |  | rainfall |  |
| dxb-2025-12 | 2025-12-18 to 2025-12-19 |  |  |  | not published |  | rainfall |  |

## Fujairah and the east coast, United Arab Emirates

`are_fujairah` · bbox 56.05, 24.95, 56.45, 25.65 (EPSG:4326)

**Mechanism.** wadi flash flooding off the Hajar mountains into a narrow coastal strip with no floodplain

**Why it is here.** Orographic lift over the Hajar concentrates the heaviest rainfall in the country here, and seven wadis converge on Fujairah city alone ([source](https://www.mdpi.com/2073-4441/15/15/2802))

**Where it floods first.** Masafi; Fujairah port and city; Kalba; Khor Fakkan; Rul Dadna. Seven wadis reach Fujairah city: Hayl, Saham, Farfar, Ham, Yabsah, Madhab, Safad

**Exposure.** [316,790 people](https://www.wam.ae/en/article/hszrh5ch-population-the-emirate-fujairah-reached-316790) over a 1,580 km² catchment.

| Event | Dates | Peak 24h rain (cm) | Event total (cm) | Station | Inundated area (km²) | Area method | Driver | Deaths |
|---|---|---|---|---|---|---|---|---|
| fjr-2020-01 | 2020-01-09 to 2020-01-12 |  |  |  | not published |  | rainfall |  |
| fjr-2022-07 | 2022-07-26 to 2022-07-29 |  | [22.2](https://en.wikipedia.org/wiki/2022_United_Arab_Emirates_floods) `V3` | Fujairah Port | not published |  | rainfall | 7 |
| fjr-2024-04 | 2024-04-14 to 2024-04-17 | [23.3](https://www.nature.com/articles/s41598-026-53055-9) `V2` |  | Kalba | not published |  | rainfall |  |
| fjr-2024-10 | 2024-10-23 to 2024-10-25 |  |  |  | not published |  | rainfall |  |
| fjr-2025-12 | 2025-12-18 to 2025-12-19 |  |  |  | not published |  | rainfall |  |

## Ganges-Brahmaputra delta, Bangladesh

`bgd_gbm` · bbox 88.0, 21.5, 92.7, 26.0 (EPSG:4326)

**Mechanism.** monsoon riverine flooding off three Himalayan rivers, with haor flash floods in the northeast

**Why it is here.** One of the lowest and most densely populated large landmasses on earth, sitting where three Himalayan rivers meet and downstream of Cherrapunji ([source](https://www.thedailystar.net/environment/climate-crisis/natural-disaster/news/sunamganj-floods-have-surpassed-all-previous-records-3049551))

**Where it floods first.** Sunamganj Sadar; Tahirpur; Bishwambarpur; Chhatak; Doarabazar in the Sylhet haor basin. Sirajganj Sadar; Kazipur; Chauhali and the Jamuna char settlements

**Exposure.** [173,600,000 people](https://en.wikipedia.org/wiki/Ganges_Delta) over a 105,000 km² catchment.

| Event | Dates | Peak 24h rain (cm) | Event total (cm) | Station | Inundated area (km²) | Area method | Driver | Deaths |
|---|---|---|---|---|---|---|---|---|
| bgd_gbm_2004 | 2004-07-01 to 2004-09-30 |  |  |  | not published |  | rainfall |  |
| bgd_gbm_2007 | 2007-07-03 to 2007-08-15 |  |  |  | not published |  | rainfall | 405 |
| bgd_gbm_2017 | 2017-08-12 to 2017-08-31 |  |  |  | not published |  | rainfall | 114 |
| bgd_gbm_2022_sylhet | 2022-05-17 to 2022-06-24 | [18.5](https://www.thedailystar.net/environment/climate-crisis/natural-disaster/news/sunamganj-floods-have-surpassed-all-previous-records-3049551) `V3` |  | Sunamganj (BMD station) | [420](https://data.humdata.org/dataset/water-extent-over-sylhet-and-sunamganj-districts-sylhet-division-bangladesh-as-of-25-may-2) | UNOSAT satellite-derived water extent, Sylhet & Sunamganj districts only, as of 25 May 2022 (pre-monsoon early stage of the event; analyzed area ~730 km2); the later mid-June flash-flood peak (185mm/24h at Sunamganj, 42 deaths, 84–94% of Sylhet/Sunamganj districts reported submerged) was NOT separately satellite-quantified in a source I could verify, so this km2 figure is a lower bound, not the peak extent | rainfall | 42 |
| bgd_gbm_2024_feni | 2024-08-21 to 2024-08-30 |  | [164.6](https://www.tbsnews.net/features/panorama/august-2024-floods-bangladesh-and-tripura-nexus-erratic-rainfall-vanishing) `V3` |  | [8,100](https://geo.btaa.org/catalog/007de930-02e7-4b32-8a6c-774c86eb2c8f) | UNOSAT/Copernicus satellite-detected flood water extent, national analysis area ~140,000 km2, product "Satellite detected water extents between 28 August & 4 September 2024" | rainfall | 71 |

## Lower Indus, Sindh, Pakistan

`pak_sindh` · bbox 66.5, 23.5, 71.5, 28.5 (EPSG:4326)

**Mechanism.** monsoon riverine flooding of the Indus mainstem, ponding on a flat irrigated plain with nowhere to drain

**Why it is here.** The 2010 and 2022 floods each inundated tens of thousands of square kilometres of the same province inside twelve years ([source](https://en.wikipedia.org/wiki/2022_Pakistan_floods))

**Where it floods first.** Dadu; Johi; Mehar; Khairpur Nathan Shah; Qambar Shahdadkot; Larkana district

**Exposure.** [55,696,147 people](https://en.wikipedia.org/wiki/Sindh) over a 140,914 km² catchment.

| Event | Dates | Peak 24h rain (cm) | Event total (cm) | Station | Inundated area (km²) | Area method | Driver | Deaths |
|---|---|---|---|---|---|---|---|---|
| pak_sindh_2010 | 2010-07-26 to 2010-09-30 |  |  |  | [37,280](https://earthobservatory.nasa.gov/images/50018/flood-extent-in-pakistan) | satellite/remote-sensing-derived flood-inundation extent, all of Pakistan (not Sindh-specific) | rainfall | 1,985 |
| pak_sindh_2011 | 2011-08-11 to 2011-09-14 |  | [129.0](https://en.wikipedia.org/wiki/2011_Sindh_floods) `V3` | Mithi | [12,988](https://en.wikipedia.org/wiki/2011_Sindh_floods) | sum of per-district figures reported as "area affected (km2)" for the six worst-hit of 23 inundated Sindh districts (Badin 3820.39, Sanghar 2494.18, Dadu 1887.57, Mirpur Khas 1836.26, Shahdadkot 1597.50, Jacobabad 1352.32 km2), said to represent 61% of total inundated area; source does not make explicit whether these are inundated extents or full administrative district areas | rainfall | 434 |
| pak_sindh_2022 | 2022-06-14 to 2022-10-31 |  |  |  | [25,000](https://reliefweb.int/report/pakistan/2022-pakistan-floods-assessment-crop-losses-sindh-province-using-satellite-data) | Sentinel-1 satellite-derived flooded-cropland/land assessment specific to Sindh province, "over 18% of Sindh's total area" (2.5 million hectares) | rainfall | 799 |

## Middle Yangtze, Wuhan and Poyang, China

`chn_yangtze` · bbox 113.5, 28.0, 117.0, 31.5 (EPSG:4326)

**Mechanism.** monsoon runoff concentrated through the Yangtze mainstem and backed up into its floodplain lakes

**Why it is here.** Poyang and Dongting act as the Yangtze's overflow storage, and the cities on their shores sit below the flood stage the river reaches in a heavy monsoon year ([source](https://en.wikipedia.org/wiki/2020_China_floods))

**Where it floods first.** Wuhan riverfront; Poyang Lake shoreline counties in Jiangxi; Dongting Lake dike districts in Hunan

**Exposure.** [13,739,000 people](https://en.wikipedia.org/wiki/Wuhan) over a 8,494 km² catchment.

| Event | Dates | Peak 24h rain (cm) | Event total (cm) | Station | Inundated area (km²) | Area method | Driver | Deaths |
|---|---|---|---|---|---|---|---|---|
| chn_yangtze_2016 | 2016-07-01 to 2016-07-06 |  | [57.0](https://en.wikipedia.org/wiki/2016_China_floods) `V3` | Wuhan (citywide) | not published |  | rainfall | 27 |
| chn_yangtze_2020 | 2020-06-01 to 2020-08-22 |  |  |  | not published |  | rainfall | 14 |
| chn_yangtze_2024_dongting | 2024-07-05 to 2024-07-08 |  |  |  | [48.0](https://www.globaltimes.cn/page/202407/1315657.shtml) | direct measurement of inundated area behind the breached Dongting Lake dyke (Tuanzhou area), average water depth ~5m, per Chinese state/local media reporting | levee_failure | 0 |
