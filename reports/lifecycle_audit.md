# Construction and Replacement Cash Flows

Status: PASS_WITH_LIMITATIONS

| Case | Construction years | Replacements | NPV billion EUR_2024 | Break-even EUR_2024/MWh |
|---|---:|---:|---:|---:|
| LC001 | 0 | 0 | 2.591 | 170.14 |
| LC002 | 5 | 0 | -0.283 | 204.79 |
| LC003 | 5 | 7 | 0.091 | 198.51 |
| LC004 | 5 | 7 | -0.818 | 213.42 |
| LC005 | 5 | 7 | -1.727 | 228.32 |
| LC006 | 7 | 7 | -2.158 | 241.29 |

LC001 reproduces the original simplified model; other cases change the declared model boundary.

Shares paid at t=0..C-1; COD=C; first annual operating receipts at C+1.

Exact outage-start times; annual buckets retain component-specific discounting.

## Limitations

- Construction durations, spending shares and replacement costs are uncalibrated analyst scenarios, not Proxima budgets or schedules.
- Engineering cases interpret fixed/variable OPEX as routine expenses excluding separate major replacements; this allocation is not empirically established.
- Explicit operating windows replace the long-run CF loss; other downtime and load remain averaged within those windows.
- No extra debt-interest/IDC charge is added to the unlevered DCF. Financing, taxes, decommissioning, offline power purchases and terminal value remain excluded.
- LC003 zero replacement cost is a diagnostic; a delay case holds spending and other costs fixed and omits real delay overhead/overruns.
- No replacement is purchased at retirement; an outage starting earlier incurs full replacement cost even if its duration extends beyond retirement.
