# Validation record: score status model

October 26–27, 2026 · Result: 10 of 10 tests passed · Synthetic records only; no client data existed or was affected.

## Method

Expected values were worked out by hand before each step and compared with the live records afterwards.

| Test | Condition | Expected | Result |
|---|---|---|---|
| T1 | Reading 1 issued, reading date one year earlier | Valid-until date one year after the reading date; flagged as due to lapse; no score change; 365-day reminder due | Pass |
| T2 | Reading 2 created with no status and a prior score of 42 | Valid-until date and score change stay blank until issued | Pass |
| T3 | Reading 2 issued | Valid-until date one year out; score change 0 − 42 = −42; status change logged | Pass |
| T4 | Reading 1 superseded | Lapse flag and reminder cleared; status change logged | Pass |
| T5 | Reading 2 withdrawn | Other values unchanged; status change logged | Pass |
| T6 | Status requests with a bad bot-check token, no token, the spam trap filled, or an invalid record ID | Rejected with HTTP 400; nothing stored | Pass |
| T7 | Status request from staging with a real bot check | Stored as New; alert sent; HTTP 200 | Pass |
| T8 | Request page at 320 px wide | No sideways scrolling | Pass |
| T9 | Scheduled reminder run (5:45 am) | Reminder sent once; recorded as sent | Pass (ran 5:45 am, October 27) |
| T10 | Scheduled lapse run (6:00 am) | Status set to Lapsed with its reason; logged | Pass (ran 6:02 am, October 27) |

## Findings

- **F1.** A status set at the moment a record is created is not logged, because the log watches changes. In normal use the status is set later, on an existing record, so it is logged. Open, low risk.
- **F2.** The request page first sent an empty spam-trap field with every request, and the route read it as spam. Fixed by sending the field only when it is filled.
- **F3.** The scheduled reminder and lapse automations could not be run on demand, so T9 and T10 ran on their real schedule the next morning. Both passed.
