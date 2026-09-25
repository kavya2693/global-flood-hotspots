# global-flood-hotspots

[![ci](https://github.com/kavya2693/global-flood-hotspots/actions/workflows/ci.yml/badge.svg)](https://github.com/kavya2693/global-flood-hotspots/actions/workflows/ci.yml)
[![license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A flood-impact dataset for twelve of the world's worst flood regions, and the
finding that came out of building it: for 96% of these floods, nobody published
both of the two numbers you would need to connect rainfall to consequence.

## The problem

Someone has to decide how much drainage to build. A city engineer in Sharjah, a
planner in Lokoja, an insurer pricing a portfolio in Houston — they all face the
same question in some form: if a storm drops this much rain on us, how much of
the city ends up under water?

It sounds like a question with an empirical answer. Floods happen constantly,
they are reported heavily, and both quantities are measurable. Rainfall is
gauged by national met services as a matter of routine. Inundated extent is
mapped from satellites by agencies who publish the results. Twenty-five years of
this should have produced a large table of storms and their consequences that
anyone could fit a curve through.

It has not. That table does not exist, and this repository is an attempt to
build it that documents exactly where it breaks.

## Why it is hard

Not measurement difficulty. Both numbers are produced routinely and to a high
standard. The obstacle is that they are produced by different institutions
responding to different kinds of flood, and those institutions are not looking
at the same places.

A meteorological service runs a gauge network that is densest where the people
are, so a city flood gets an excellent rainfall record. But urban flooding is
shallow, brief, and happens underneath buildings and trees, which is close to
the worst case for satellite water detection, and it rarely triggers the
international mapping activations that produce a published extent.

Riverine flooding on a flat agricultural plain is the mirror image. It covers
thousands of square kilometres of open ground for weeks, which synthetic
aperture radar maps easily and which reliably triggers a UNOSAT or Copernicus
activation. But those plains are gauge-poor, and the rainfall that caused the
flood fell days earlier in a mountain catchment hundreds of kilometres upstream
where nobody was measuring.

So the rainfall and the extent tend to exist for different floods. Not by
accident, and not evenly.

## The approach

Twelve regions were selected on people affected by flood disasters over
2000-2025, weighted by recurrence: ten chosen on global impact and two in the
UAE. For each, every flood event since 2000 that could be documented was
recorded, with every numeric figure carrying a resolvable source URL and an
evidence tier. Figures without a source were dropped rather than estimated.

The key decision was to write the validator first. Before any data existed,
`src/floodhotspots/validate.py` was written and tested against deliberately
broken tables: a figure with no URL, a figure with a URL that is really a
citation string, an inferred figure with no explanation, an area with no
measurement method, rainfall entered in centimetres where millimetres belong.
The dataset was then built to pass it. This ordering is why the coverage numbers
below can be trusted — nothing entered the table by being plausible.

## The result

The model this project set out to fit does not exist, because the data to fit it
does not exist.

| | |
|---|---|
| Regions | 12 (10 global, 2 UAE) |
| Flood events documented, 2000-2025 | 46 |
| Events with a sourced peak 24-hour rainfall | 11 (24%) |
| Events with a sourced inundated area | 13 (28%) |
| **Events with both** | **2 (4.3%)** |
| Events admissible for a rainfall-to-extent regression | **2** |

Two observations. `floodhotspots model` raises `NotEstimable` and fits nothing,
because a number produced from two observations is not a weak result, it is not
a result.

The interesting part is that the 4.3% is not what you get from two independent
28% and 24% coverages. Independence would predict about 7%, and more importantly
it would predict the gaps falling randomly across sites. They do not:

| Site | Flood type | Rainfall coverage | Extent coverage |
|---|---|---|---|
| Mumbai | urban pluvial | 0.80 | 0.00 |
| Jakarta | urban pluvial | 0.60 | 0.00 |
| Ahr valley and Rhine-Meuse | urban pluvial | 0.50 | 0.00 |
| Dubai and Sharjah | urban pluvial | 0.20 | 0.20 |
| Fujairah and the east coast | urban pluvial | 0.20 | 0.00 |
| Ganges-Brahmaputra delta | riverine | 0.20 | 0.40 |
| Houston, Harris County | urban pluvial | 0.00 | 0.20 |
| Mekong delta | deltaic | 0.00 | 0.50 |
| Rio Grande do Sul | riverine | 0.00 | 0.50 |
| Middle Yangtze | riverine | 0.00 | 0.33 |
| Niger-Benue, Lokoja | riverine | 0.00 | 0.75 |
| Lower Indus, Sindh | riverine | 0.00 | 1.00 |

**Spearman rho between a site's rainfall coverage and its extent coverage:
-0.81, p = 0.0013, n = 12 sites.** Strongly negative. A site tends to have one
measurement or the other, and which one it has is predicted by what kind of
flooding it gets.

Sindh is the clearest case: three events, every one with a satellite-derived
extent, not one with a sourced 24-hour station rainfall. Mumbai is the exact
inverse: four of five events with a station rainfall figure, not one with a
mapped extent, in a city that floods severely every single monsoon.

### The number that disappoints

The evidence quality is lopsided in the opposite direction to the coverage. Of
the 13 extents, 11 are tier V1 or V2 — satellite-derived or official. Of the 11
rainfall figures, only 3 are. The rainfall record here is mostly newspapers
quoting a met service, not the met service's own bulletin. Several primary hosts
(ReliefWeb, UNOSAT, Humanitarian Data Exchange, the NHC report PDFs) refused
automated retrieval during collection, so figures that certainly exist at V1 are
carried here at V3 or not at all. The measured 24% rainfall coverage is
therefore a floor on what is genuinely public, not a ceiling. That weakens the
headline claim and is stated here rather than left to a reader to notice.

### What the twelve regions look like

The per-site analysis the dataset supports — dominant mechanism, the
neighbourhoods that flood first, peak rainfall in centimetres, inundated area
where it exists — is generated into
[`reports/site-profiles.md`](reports/site-profiles.md). The one extent published
for either UAE site is 23.8 km² for Dubai in April 2024, from a PlanetScope
U-Net classification in *Annals of GIS*. There is no published inundated area
for any Fujairah east-coast event, including July 2022.

## How it works

```
data/raw/sites.csv     12 regions: bbox, mechanism, exposure, hotspot sub-areas
data/raw/events.csv    46 events: rainfall, extent, casualties, driver, sources
        |
        v
validate.py            every figure needs a URL, a tier, and a method.
                       no figure passes on plausibility.
        |
        v
coverage.py            what the record contains, by figure, by site, by
                       flood type. this is the result.
        |
        v
features.py            joins, logs, and marks each event admissible or not
        |
        v
model.py               leave-one-site-out. refuses to score below 3 sites.
```

Two exclusion rules decide what a regression may see, and both keep the excluded
rows in the dataset rather than deleting them:

- **Driver.** A dam or levee failure sets the extent independently of the
  rainfall. Jakarta 2013 (West Flood Canal dike breach) and the 2024 Dongting
  breach are recorded and excluded from any fit.
- **Method.** An administrative district area is not an inundated extent. Jakarta
  2007's "75% of the city" is recorded with its method stated and excluded.

Every exclusion and its reason is written to
[`reports/excluded-events.md`](reports/excluded-events.md).

## Running it

From a clean clone, with no accounts and no downloads:

```bash
pip install -r requirements.txt
PYTHONPATH=src python -m floodhotspots run
```

That validates the tables, prints the coverage audit, builds the feature table,
attempts the model, and regenerates every file in `reports/`. Subcommands
`validate`, `coverage`, `features`, `model` and `report` run the stages
individually. Or `docker build -t floodhotspots . && docker run floodhotspots`.

## The data

Every figure was collected from public sources and carries the URL it came from
in the same row. Evidence tiers: **V1** satellite-derived extent or official
gauge record, **V2** government or UN agency report, **V3** reputable secondary
reporting, **I** inferred with a mandatory explanatory note.

Of the 13 extents that exist, the measurement methods do not agree with each
other:

| Measurement method | Events |
|---|---|
| Satellite, unspecified sensor | 5 |
| Satellite SAR (Sentinel-1) | 2 |
| Hydraulic model output | 2 |
| Government estimate | 1 |
| Administrative district area, not an extent | 1 |
| Other | 2 |

Pooling these into one regression target would have been incoherent even with
enough rows, which is why `area_method` is a required column rather than a note.

`scripts/fetch_rainfall.py` (ERA5) and `scripts/fetch_terrain.py` (Copernicus
GLO-30) will re-derive rainfall and elevation independently for anyone with
credentials. Both refuse to run without them rather than degrading quietly. The
default pipeline does not read their output.

Sites were selected on people affected 2000-2025 weighted by recurrence.
Rejected under that criterion: **Derna, Libya 2023** — the extent was set by two
dam failures, so including it would have put a row in the table where the
rainfall-to-extent relationship does not exist. **Valencia 2024** and **Kerala
2018** — severe, but single events that fail the recurrence half of the
criterion. **Bangkok 2011** — would have displaced Jakarta with a near-identical
mechanism.

## Tests

57 tests, none of which require the dataset. The two that matter most:

`test_validate.py::test_figure_with_non_url_source_is_rejected` feeds the
validator the string `"Reuters, April 2024"` in a source column. That is what an
unsourced figure looks like in practice — not a blank cell, but a citation that
reads like provenance and cannot be checked. It has to be rejected, and this
test is why the coverage numbers mean anything.

`test_model.py::test_median_baseline_is_anti_informative_across_sites` asserts
that the baseline's Spearman is *negative*, which is counterintuitive enough to
be worth pinning. Under leave-one-site-out, holding out the largest-extent site
removes its values from the training median, so the prediction moves away from
the truth. The baseline is not a neutral reference point under this split, and
anything compared against it has to clear that.

## Known limitations

**The biggest gap: the rainfall coverage figure is a floor, not a measurement.**
ReliefWeb, UNOSAT, Humanitarian Data Exchange and the NHC tropical cyclone
report PDFs all refused automated retrieval during collection. Figures that are
genuinely public are consequently missing or downgraded here. A collection pass
with working access to those hosts would raise the 24% and might raise the 4.3%.
The direction of the coverage anti-correlation is unlikely to flip — Sindh's
absent gauge data is a real absence, not a fetch failure — but its magnitude is
not firm.

Beyond that:

- 46 events is not an exhaustive census. It is what could be documented to this
  provenance standard, which under-counts smaller floods everywhere and
  under-counts every flood in the gauge-poor and press-poor regions worst.
- Reporting bias is not corrected anywhere. An event enters this dataset because
  someone wrote about it, and the same attention that produced the write-up
  plausibly produced the measurement.
- Mean elevation is in the schema and empty for all twelve sites. No source
  states an areal-mean elevation for any of them, so the column is dropped from
  the feature set at runtime rather than imputed.
- Site boundaries are working definitions, not published administrative
  geometry. Several are the researcher's bounding box over the flood-affected
  area and are labelled as such.
- Population figures mix census years and definitions (city, metro, province)
  across sites and are not comparable between them.
- The two UAE sites are the thinnest in the set for exposure figures, because
  almost every published UAE flood impact number is a national total rather than
  an emirate-level one.

## Insights and learning

I picked this problem expecting the hard part to be the modelling. It was not.
The hard part was that the dataset I assumed existed does not, and the most
useful thing I could do was establish that carefully rather than paper over it.

The moment that changed the project was reading the first research file back and
noticing that Mumbai had four rainfall figures and zero extents, while a later
file had Sindh with three extents and zero rainfall. My first instinct was that
the collection was uneven and needed another pass. It was not uneven. It was
measuring something real about who measures floods and why, and the
anti-correlation across all twelve sites turned out to be strong and
significant. The thing I nearly filed as a data-quality problem was the result.

Writing the validator before the data was the decision that made the rest
possible. Every coverage number in this README is a count of rows that survived
a check written before anyone knew what the data would look like, which is the
only reason I am willing to put 4.3% in a table and defend it. Had I collected
first, the pressure to accept "Reuters, April 2024" as a source in order to fill
a row would have been considerable, and the headline number would have been
quietly wrong.

I also got the baseline wrong and the test caught it. I asserted that a median
baseline would have no rank skill, reasoning that a constant cannot order
anything. Under leave-one-site-out the baseline is not constant — it is the
median of the eleven sites you kept — and it is actively anti-informative. The
test failed, I assumed my code was broken, and it was my mental model that was
broken. That is now a test with a docstring rather than a footnote.

What I would do next is narrower than what I started with. Rather than another
global sweep, I would take the Dubai April 2024 event, which is the one UAE flood
with both a rainfall record and a published extent, and reproduce the 23.8 km²
figure independently from Sentinel-1. If a single analyst can produce an extent
for one event in a week, then the reason 96% of these floods lack one is not
technical difficulty, and the interesting question becomes institutional rather
than hydrological.

## License

MIT. See [LICENSE](LICENSE).
