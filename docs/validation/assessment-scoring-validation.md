# Validation record: assessment scoring

August 21, 2026 · Synthetic records only.

## What was tested

The full chain from each response to the final score: response → question → dimension → dimension total → weighted composite → maturity band → risk signal. Each dimension carries an explicit, equal weight, which replaced implicit weighting by question count, a known pitfall in composite indicator design.

## Method

A synthetic assessment was linked to one response per question, with each question checked to be distinct and none duplicated. Three conditions were run against the live system, with expected values worked out by hand first:

| Test | Condition | What it proves |
|---|---|---|
| P-1 | Every response at the maximum | Each dimension filter matches its questions; the formula reaches its ceiling exactly |
| P-2 | Every response at the minimum | The formula floor; the risk signal fires across all designated questions |
| P-3 | Mixed scores by dimension | Partial-score arithmetic across all dimensions at once; the risk signal stays silent |

Every dimension result, the composite score, the band and the risk signal matched the expected values.

## The defect it found

Two dimensions had wrong maximum scores: one was understated by 5 points and the other overstated by 5. Because the errors cancelled, the instrument's total maximum was still correct, so no check on the total could have caught it. The defect had passed five weeks of review because that review confirmed the data moved correctly, not that the values being moved were arithmetically sound.

Had it reached a client, every score would have understated one area of exposure and overstated another, while presenting a total that looked right. It was found by checking the arithmetic against the live system rather than against the documentation describing it.

*Dimension names, maximums, weights and question wording are proprietary and not published here.*
