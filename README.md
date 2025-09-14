# DM Lawncare – Operational Command Center

This repository powers the full operational logic for DM Ride-On Lawn Care, including:

- Quote engine with booking evaluation and consent logic
- Dispatch dashboard for daily workload and job status
- Admin panel for wages, costs, and taxation tracking
- Monitoring tools for uptime and form activity
- End-of-day reporting and care network integration

## Modules

### Quote Engine
Located in `/quote-engine/`, this form captures client requests, evaluates booking feasibility, applies travel fees, and logs data to Sheets or dispatch.

### Admin Panel
Located in `/admin-panel/`, this dashboard provides full oversight of quotes, jobs, wages, tax summaries, and monitoring alerts.

### Data Hooks
Located in `/data-hooks/`, these endpoints connect to Google Sheets, Firebase Auth, and optional email/SMS triggers.

### Reports
Located in `/reports/`, this module generates daily summaries, flags delays, and supports care network billing.

## Setup

1. Clone the repo: `git clone https://github.com/Dmxshock/dm-lawncare.git`
2. Deploy `quote-engine.html` to your hosting environment
3. Configure `appsScriptWebhook.md` with your Google Sheets endpoint
4. Set up Firebase Auth for secure admin access
5. Customize `wageTaxModule.js` with your operator rates and GST logic

## Roadmap

- [ ] Add grouped job routing logic
- [ ] Integrate photo proof uploader
- [ ] Build care network billing module
- [ ] Expand dispatch calendar with slot previews


