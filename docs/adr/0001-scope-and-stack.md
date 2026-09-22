# ADR-0001: Scope, dataset strategy and modelling target

Status: accepted
Date: 2026-09-22

## Context

The brief was to identify flood hotspots across the ten most flood-affected
regions in the world plus two in the UAE, and to report, per site, where it
floods, how much rain fell in centimetres, and how much area was affected.

Three things about that brief are harder than they look.

"The ten most flood-affected regions" is not a fact waiting to be looked up.
Ranked by deaths you get one list, by people affected another, by economic loss
a third, and by recurrence a fourth. Any list presented without its criterion is
an opinion wearing a number.

"Affected area" is not one measurement. A Sentinel-1 derived inundation
polygon, a government damage survey and a newspaper's "an area the size of
Switzerland" are three different quantities. They are routinely quoted
interchangeably.

"Rainfall in centimetres" is ambiguous between the peak 24-hour depth, the
event total and the multi-day antecedent total, which for a monsoon flood can
differ by a factor of five.

## Decision

**Ranking criterion.** Sites are selected on people affected by flood disasters
over 2000-2025, weighted by how often the region floods. The criterion is stated
in the README and the sites a different criterion would have chosen are named as
rejected, with the reason.

**Unit of observation is the event, not the site.** Twelve sites is not a
dataset. Twelve sites contributing four to eight documented events each is a
small but workable one, and it lets the model see the same catchment under
different rainfall, which is the only way rainfall can be separated from basin
size.

**Data strategy: curated and cited, with optional fetchers.** The dataset is a
committed CSV where every numeric figure carries a resolvable source URL and an
evidence tier. `scripts/fetch_rainfall.py` and `scripts/fetch_terrain.py` will
re-derive rainfall and terrain from ERA5 and Copernicus GLO-30 for anyone with
credentials, and refuse to run without them. The repo therefore works from a
clean clone with no accounts, which the alternative did not.

**Rainfall definition is fixed at peak 24-hour station depth**, stored in
millimetres and converted to centimetres exactly once, in the report layer.
Sources that give only a multi-day total populate a separate column and leave
the 24-hour column empty. Nothing is converted by estimation.

**Modelling target is log10 inundated area in square kilometres.** Extent spans
four orders of magnitude across these sites; an unlogged target would be a model
of the Indus basin with eleven outliers attached.

**Validation is leave-one-site-out.** Events at the same site share a catchment,
a drainage standard and a reporting agency. A random split would hand the test
set rows whose neighbours the model had already memorised.

**Rows whose extent was not produced by rainfall are excluded from the fit and
kept in the dataset.** A dam or levee failure decouples extent from rainfall
depth. So does an area figure that is really an administrative district total.
Both are listed in `reports/excluded-events.md` rather than quietly deleted.

## Alternatives rejected

**Full satellite pipeline from Sentinel-1.** Deriving every extent ourselves
would give one consistent measurement method and remove the heterogeneity
problem entirely. It also requires multi-gigabyte downloads, two registered
accounts and a SAR water-classification step that is a project in itself. The
heterogeneity is instead handled by recording the method per row and testing
whether excluding the weaker tiers changes the result.

**Flood susceptibility classification per grid cell.** The more conventional
framing, and the one with more prior art. Rejected because it answers a
different question: susceptibility maps say where water goes, not how much area
a given storm will cover, and the brief asked about rainfall and extent.

**Hotspot clustering.** Unsupervised, quick, and nothing to defend. Rejected as
too thin for the purpose.

**Including Derna, Libya 2023.** Severe and recent, but the extent was set by
two dam failures. Including it would put a row in the training set where the
rainfall-to-extent relationship does not exist, which is exactly the error this
project is trying to avoid making.
