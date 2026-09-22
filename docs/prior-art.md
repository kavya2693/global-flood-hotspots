# Global Flood Hotspots — Prior Art Survey

**Compiled:** 2026-09-22. **Method:** every repo below was confirmed with a live `gh api repos/<owner>/<name>` call on 2026-09-22, or (where marked) carried over from a live verification on 2026-09-20 documented in `flood360/research/repo-scout.md`. Stars, licence (SPDX) and last-push date are measured values from those responses. Nothing below was recalled from memory without a live check.

This survey is scoped to a **data/ML flood-hotspot project** — regressing or classifying flood risk/extent/impact from terrain, rainfall and exposure features — not hydraulic simulation engines (SWMM, SFINCS, Delft3D, etc.), which are covered in the separate `flood360` hydraulic-twin report and are out of scope here.

---

## 1. Flood susceptibility mapping with ML (RF / XGBoost / logistic regression over terrain + rainfall)

| Repo | What it does | Licence | Stars | Last push | Relevance to rainfall→affected-area regression |
|---|---|---|---|---|---|
| `omarseleem92/Machine_learning_for_flood_susceptibility` | ML pipeline (RF and others) for flood susceptibility mapping from terrain/hydrology predictors | none (no LICENSE file) | 45 | 2023-02-16 | Single-site susceptibility classifier, not a cross-site rainfall regression. Predictor-engineering reference only |
| `Akajiaku11/Enhancing-Flood-Susceptibility-Mapping-with-Machine-Learning` | ML + morphometric flood susceptibility for Bayelsa State, Nigeria catchments | none | 54 | 2026-04-02 | Single-region case study. Feature list (morphometrics + rainfall + DEM) is the useful part |
| `Dogiye12/Flood-Susceptibility-Mapping-with-Morphometrics-ML` | RF/XGBoost trained on morphometric, rainfall and DEM data | none | 38 | 2025-05-26 | Closest architectural analogue found: RF/XGBoost over rainfall+terrain features, but still one basin, susceptibility (classification) not affected-area (regression) |
| `waleedgeo/FSM-PK` | Data + code for a published paper: high-resolution flood susceptibility mapping and exposure assessment in Pakistan (AI/ML + geospatial) | NOASSERTION | 15 | 2026-07-15 | Peer-reviewed methodology reference; adds exposure assessment on top of susceptibility, still single-country |
| `HydroLAB-UNIBAS/GFA-Geomorphic-Flood-Area` | Automatic DEM-based procedure for flood-prone-area detection (geomorphic, not ML) | none | 34 | 2021-09-16 | Not ML, but a common terrain-derived predictor (geomorphic flood index) other susceptibility papers use as a feature |
| `abusufian-dev/flood-early-warning-bangladesh` | Flood early-warning system using CHIRPS rainfall + ML, reports 88.7% accuracy | MIT | 1 | 2026-03-16 | Rainfall-driven ML flood model, but early-warning classification for one country, not a cross-site area-regression |

**Verdict for this category:** every susceptibility repo found is a single-site or single-country classifier (flood/no-flood pixel), built as a student project or thesis artefact (0 have CI, docs sites, or releases). None regress a continuous affected-area outcome, and none pool multiple countries/basins into one model. 6/6 candidates verified live; 0 unverified.

---

## 2. Global flood event databases and their code

| Repo | What it does | Licence | Stars | Last push | Relevance to rainfall→affected-area regression |
|---|---|---|---|---|---|
| `cloudtostreet/MODIS_GlobalFloodDatabase` | Code that produced Cloud to Street / Colorado's Global Flood Database (MODIS-derived flood extents, 2000–2018) and population-exposure change assessment | MIT | 121 | 2021-09-08 | **Most directly relevant repo in the whole survey.** This is a real global, multi-event flood-extent database with reproducible code — the closest existing thing to "affected area per event, globally." Any affected-area regression should be validated against this dataset |
| `larrynburris/FloodReport` | Small app to browse the Dartmouth Flood Observatory's Global Active Archive of Large Flood Events | none | 0 | 2017-10-20 | Dead, trivial wrapper. DFO itself (the actual global event archive with start/end dates, area, deaths) is a spreadsheet/website at Colorado, not a maintained GitHub repo |
| `luskan/floods_analysis` | Analysis combining HANZE (European historical flood impacts, 1870–2020) and Dartmouth Flood Observatory (1985–present) | none | 0 | 2024-11-16 | Small personal analysis, not tooling, but confirms HANZE + DFO as the two usable open historical-impact sources; neither has its own maintained repo |
| `IHCantabria/SWIM_WaterBalanceModule` | Streamflow analysis using ML over ERA5 + GloFAS global datasets | none | 4 | 2026-01-04 | GloFAS access pattern (ERA5 + GloFAS as ML inputs), useful as an integration reference; not itself a flood database |

**Not found / no code repo exists (checked live, confirmed absent):**
- **EM-DAT** — no GitHub code repo under any plausible name (`EM-DAT`, `emdat`, "EM-DAT python") returns disaster-database code; EM-DAT is distributed as a licensed spreadsheet export from CRED, not an open repo.
- **HANZE** — no dedicated tooling repo; only referenced inside third-party analysis notebooks (see `luskan/floods_analysis` above).
- **GloFAS** itself (ECMWF/JRC's forecasting system) has no standalone open-source repo; `ec-jrc/lisflood-code` (already verified in `flood360/research/repo-scout.md`, 169★, live 2026-09-22) is the underlying continental hydrological model GloFAS runs on, not GloFAS's own code.
- **"floodbase"** as a search term returns zero GitHub results — the commercial Floodbase product has no public repo.

**Verdict for this category:** 4/4 candidate repos verified live. Cloud to Street's `MODIS_GlobalFloodDatabase` is the one genuine, citable, multi-event global flood-extent dataset+code combination in this whole survey — treat it as the benchmark a novelty claim has to be measured against.

---

## 3. Satellite flood extent mapping datasets (Sen1Floods11, WorldFloods, Cloud to Street, UNOSAT)

| Repo | What it does | Licence | Stars | Last push | Relevance to rainfall→affected-area regression |
|---|---|---|---|---|---|
| `cloudtostreet/Sen1Floods11` | The Sen1Floods11 benchmark: 4,831 hand-labelled and weakly-labelled Sentinel-1 chips for flood-water segmentation, 11 flood events | none (no LICENSE file) | 254 | 2021-04-09 | The standard benchmark for extent *segmentation* (per-pixel flood/no-flood from SAR), not area regression from rainfall. Feeds "actual affected area" ground truth if you derive area from its extent masks |
| `spaceml-org/ml4floods` | NASA FDL/Trillium's end-to-end ecosystem: data pipelines, WorldFloods dataset access, and trained models for flood-extent segmentation from Sentinel-2 | LGPL-3.0 | 182 | 2026-05-20 | This is where the WorldFloods dataset actually lives (not a standalone `WorldFloods` repo — that name search returns only a 0-star personal fork). Most actively maintained satellite flood-extent codebase found in the whole survey |
| `spaceml-org/floodmapper` | Companion operational flood-mapping pipeline built on ml4floods | GPL-3.0 | 7 | 2024-12-10 | Smaller, less mature operational wrapper around the same WorldFloods models |
| `UNITAR-UNOSAT/UNOSAT-AI-Based-Rapid-Mapping-Service` | UNOSAT's own FCN for rapid flood segmentation from SAR (paper: Nemni, Bullock, Belabbes, Bromley) | none | 58 | 2023-08-04 | Confirms UNOSAT's actual open code — a real UN humanitarian-mapping org publishing a working model, useful as an authority citation for "how the UN maps floods from SAR" |
| `Tamer-Saleh/S1GFlood-Detection` | DAM-Net: SAR flood detection with attention-based vision transformers (ISPRS J P&RS 2024) | not checked (found via topic search, not independently verified this session — see note) | 54 | 2026-05-23 | Listed for completeness; flagged unverified-detail below since only the topic-search summary was read, not a direct `gh api` call |

**Verdict for this category:** 4/5 fully verified via direct `gh api` calls; `Tamer-Saleh/S1GFlood-Detection` was seen only in a topic search result and should be independently verified before citing. None of these repos regress affected area against rainfall — they are all extent-*segmentation* models consuming satellite imagery after a flood has already happened, which is a fundamentally different input (imagery, not rainfall/forecast data) and a fundamentally different task (pixel classification, not scalar-area regression).

---

## 4. Flood exposure / population-at-risk tooling (GHSL, WorldPop, Aqueduct Floods)

| Repo | What it does | Licence | Stars | Last push | Relevance to rainfall→affected-area regression |
|---|---|---|---|---|---|
| `wpgp/wpgpDownloadPy` | Official WorldPop Global Project toolset for finding/downloading WorldPop population rasters | NOASSERTION | 21 | 2018-12-02 | Standard population-exposure input layer; stale (2018) but WorldPop's raster format hasn't changed enough to obsolete it |
| `wpgp/wopr` | R package + Shiny app for WorldPop Open Population Repository (WOPR) API access | GPL-3.0 | 40 | 2025-04-04 | More actively maintained than wpgpDownloadPy; the better current pick for population-exposure joins |
| `wri/Aqueduct40` | WRI Aqueduct 4.0 data and methodology, including the Aqueduct Floods risk layers | NOASSERTION | 34 | 2024-09-18 | The one repo in this category that is actually about flood *risk* (not just raw population), and is the closest published methodology to "translate hazard into exposed population/assets at global scale" |
| — GHSL — | No repo found under WRI/JRC or elsewhere that *serves* GHSL data as code; every result was a personal tutorial (`milos-agathon/*`, `pablohernandezb/*`) showing how to plot GHSL rasters someone already downloaded, not an access/processing library | — | — | — | GHSL itself is JRC-distributed via their own data portal, not GitHub-hosted code |

**Verdict for this category:** 3/3 real tooling repos verified live (plus GHSL confirmed to have no dedicated access-library repo — only tutorial/plotting scripts, which are not worth listing individually). None of these repos build a rainfall-to-affected-area model; they are exposure-layer inputs a project like this would consume, not comparable prior art for the regression itself.

---

## 5. Rainfall / precipitation data access libraries (IMERG, CHIRPS, ERA5/cdsapi)

| Repo | What it does | Licence | Stars | Last push | Relevance to rainfall→affected-area regression |
|---|---|---|---|---|---|
| `ecmwf/cdsapi` | Official ECMWF Python client for the Copernicus Climate Data Store — the standard way to pull ERA5 reanalysis rainfall | Apache-2.0 | 321 | 2026-03-12 | Standard, well-maintained ingestion path for the rainfall predictor side of any global model. Most credible repo in this category |
| `ropensci/chirps` | rOpenSci's official API client for CHIRPS (and CHIRTS) rainfall data | NOASSERTION | 38 | 2026-06-23 | The one properly maintained, org-backed (rOpenSci) CHIRPS access library found — most other CHIRPS repos are one-off download scripts with 0–1 stars |
| `SERVIR/ClimateSERV2` | NASA SERVIR's platform for visualizing/downloading historical rainfall (CHIRPS-based), vegetation condition, and 180-day rainfall/temperature forecasts | NOASSERTION | 11 | 2026-06-01 | Real USAID/NASA-backed operational service with public code; useful as an alternate rainfall+forecast ingestion path, particularly for agriculture/water-availability framing |
| `aus-ref-clim-data-nci/GPM` | Code to download and manage the GPM IMERG precipitation dataset (Australian NCI reference-climate-data project) | Apache-2.0 | 2 | 2026-08-31 | Small but actively pushed (Aug 2026) and institutionally backed (NCI Australia); the most current IMERG downloader found — most IMERG results were disposable student scripts |

**Not found:** no maintained Python equivalent of `ropensci/chirps` was located (all Python "CHIRPS" hits were single-author, 0–4-star one-off download scripts); no dedicated GloFAS-access Python package beyond the ERA5+GloFAS ML repo already listed in §2.

**Verdict for this category:** 4/4 verified live. These are solid, credible ingestion libraries — the strongest-quality category in this survey — but they are infrastructure for pulling rainfall data, not models or analyses that relate rainfall to flood outcomes.

---

## Carried over from `flood360/research/repo-scout.md` (verified live 2026-09-20, ML/data-relevant subset only)

The source report is oriented toward hydraulic simulation engines and was excluded from re-verification here per scope, but these specific rows are genuinely relevant to a data/ML flood-hotspot project and are worth citing as prior art:

| Repo | What it does | Licence | Stars (as of 2026-09-20) | Relevance |
|---|---|---|---|---|
| `neuralhydrology/neuralhydrology` | LSTM-family rainfall-runoff deep learning (Kratzert/Google lineage) | BSD-3-Clause | 581 | Closest maintained code to "Google flood forecasting"; rainfall→runoff, not rainfall→affected-area, but the nearest ML architecture precedent for a rainfall-input regression |
| `kratzert/Caravan` | Global community large-sample hydrology dataset | BSD-3-Clause | 273 | Multi-basin, global-scale training data — the pattern (pool many basins/events into one dataset) a global affected-area regression would need to follow |
| `abhiramm7/openfloodhub` | Self-hostable open alternative to Google Flood Hub; per-gauge 1D CNN | Apache-2.0 | 25 | Closest open analogue to Google Flood Hub; per-gauge forecasting, not cross-site area regression, and still small/new |
| `google-research/google-research` (flood-forecasting subdirectory) | Google's flood forecasting research code, living inside their monorepo | Apache-2.0 | 38801 (whole monorepo) | Sparse-checkout only; the actual flood code is one subdirectory of a huge repo, not a standalone comparable project |
| `Deltares-research/FloodAdapt` | Intervention-and-adaptation scenario tool over SFINCS + FIAT | NOASSERTION | 18 | Scenario/impact comparison tool, but requires running a hydraulic solver per scenario — not a direct rainfall→area statistical regression |
| `Deltares/Delft-FIAT` | Depth-damage-over-exposure impact assessment | MIT | 7 | Converts a depth raster (from a solver) into damage/affected figures — downstream of a hydraulic run, not a substitute for one |
| `NOAA-OWP/inundation-mapping` | Operational HAND-based US flood inundation mapping | Apache-2.0 | 131 | Operational, US-only, HAND-based (topographic index), not a global rainfall regression, but its validation harness is worth studying |

---

## The gap

No open repo found in this survey — across five ML/data-focused categories plus the hydraulic-engine report's ML section — regresses flood-affected area against rainfall across multiple global sites with per-figure source provenance. What exists instead falls into four buckets, none of which is this project: (1) single-site or single-country ML **susceptibility classifiers** (flood/no-flood pixel probability), built almost entirely as thesis or student artefacts with no shared benchmark or cross-site pooling; (2) satellite **extent-segmentation** models (Sen1Floods11, WorldFloods/ml4floods, UNOSAT) that classify pixels from post-event imagery, an entirely different input (imagery, not rainfall) and output (mask, not scalar area); (3) **hydraulic-solver pipelines** (FloodAdapt, Delft-FIAT, NOAA HAND mapping) that require running an actual physics model per scenario, which is the opposite of a lightweight statistical regression; and (4) **infrastructure libraries** (cdsapi, CHIRPS/IMERG downloaders, WorldPop, Aqueduct) that supply inputs but perform no modeling themselves. The one repo that comes closest to a real "global, multi-event, area-based" dataset is Cloud to Street's `MODIS_GlobalFloodDatabase` (121★, MIT, code that produced the actual paper) — it has global multi-event flood extents and population-exposure changes, but it does not regress against rainfall as a predictor; it is a satellite-derived outcome archive, not a rainfall-driven model. `neuralhydrology` and `Caravan` show the closest architectural and data-pooling pattern (multi-basin, rainfall-driven, deep learning) but predict streamflow/runoff, not affected area. Based on this survey, the novelty claim survives: the specific combination of (a) rainfall as the sole predictor, (b) affected area as the regression target, (c) multiple global sites in one model, and (d) per-figure source provenance does not appear to exist as an open repo. This is not proof of absence — closed/commercial systems (Floodbase, Jupiter Intelligence, insurance-industry cat models) plausibly do something similar behind paywalls, and academic papers may describe similar regressions without a public repo — but nothing citable and open contradicts the claim.
