# Validation record: launch, booking, payments and invoicing

October 24 to November 1, 2026 · Tests used synthetic requests or the owner's own transactions; no client data existed or was affected.

## Website launch (October 27, 2026)

| Gate | Result |
|---|---|
| Pre-launch go/no-go audit (October 24): seven blockers found | All seven closed before launch |
| Production smoke test, 21 sitemap pages | Every page returned 200 with one heading, title, description and canonical URL; internal links worked; root domain redirected to www; robots.txt allowed crawling; no cookies set |
| Accessibility and layout checks (pre-launch) | axe-core on 20 pages; layout checked at 14 screen sizes |
| One live request from each form | Records created, dates held, confirmations and alerts sent; test data removed |
| Sitemap submitted to Google Search Console | Success, 21 pages |

## Booking and calendar invitations

| Check | Result |
|---|---|
| A request places a private, tentative hold on the owner's calendar; nothing goes to the requester | Pass |
| Confirm sends exactly one Outlook invitation with a Teams link | Pass |
| Decline sends a branded "date not available" email and reopens the time | Pass |
| A decision cannot be sent twice (two guard checks) | Pass |
| Acknowledgement email and Teams alert wording | Pass |
| Releasing a date and its calendar hold | Pass |
| Hold lapses and the requester is told | Pass (observed October 28, 29 and 30) |
| 7:00 am reminder of an unconfirmed hold | Pass (observed October 28) |
| Calendar clash: nothing sent, owner told | Pass |

## Live payments (November 1, 2026)

| Check | Result |
|---|---|
| Restricted API key with least privilege, live webhooks | Built and checked |
| A real $1 invoice: sent, paid by the owner, refunded | Each step recorded automatically on the request |

## Automated invoicing (November 1, 2026)

| Check | Result |
|---|---|
| Rule logic (13 cases): due dates, payment methods, late bookings, missing data, open-invoice block | Pass |
| Live drafts at $1, $9,500, and $20,000 less a $9,500 workshop credit | Pass; drafts only, nothing sent |
| Owner sends a draft from Stripe; the request updates to Invoiced | Pass |
| Second Create on the same request is refused | Pass |
| Voided test invoice updates the request to Void | Pass |

## Intake reliability

From the integration platform's run history: 25 of 25 runs of the website intake route completed successfully from October 18 (after a credential fix) to October 31, 2026. All were test submissions.
