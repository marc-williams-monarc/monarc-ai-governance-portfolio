"""Recount the open-items metrics quoted on the résumé from the register data.

Inclusion rules (stated so the number can be checked):
- Counts every item struck in the "Struck this cycle" table of register
  versions 9 to 15 (October 12 to 24, 2026), the versions on file.
- Version 13 repeated version 12's table on the same day; it is counted once.
- An item closed in two versions (WEB-4) counts once.
- Days to close are measured only for items first listed and closed inside the
  window, using version dates (accurate to the day). Items opened and closed
  in the same version are reported separately.
"""
import csv
import statistics
from datetime import date
from pathlib import Path

rows = list(csv.DictReader(open(Path(__file__).parent / "data" / "register_closures.csv")))
unique = {r["ref"] for r in rows}
print(f"Closure rows: {len(rows)}; unique items closed: {len(unique)}")
start = min(date.fromisoformat(r["closed_on"]) for r in rows)
end = max(date.fromisoformat(r["closed_on"]) for r in rows)
print(f"Window: {start} to {end} ({(end - start).days} days)")

days, same = [], []
for r in rows:
    if r["first_listed_on"]:
        d = (date.fromisoformat(r["closed_on"]) - date.fromisoformat(r["first_listed_on"])).days
        (same if d == 0 else days).append((r["ref"], d))
vals = [d for _, d in days]
print(f"Items with both dates: {len(days)}; median days to close: {statistics.median(vals)}; "
      f"mean: {statistics.mean(vals):.1f}; range {min(vals)}-{max(vals)}")
print(f"Opened and closed in the same version: {len(same)} ({', '.join(r for r, _ in same)})")
