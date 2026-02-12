#!/usr/bin/env python3
"""Fetch GA4 data for CareK9 and save to data.json"""
import json, os, subprocess, tempfile
from datetime import datetime, timedelta

# Get service account from AWS Secrets
secret = json.loads(subprocess.check_output([
    'aws', 'secretsmanager', 'get-secret-value',
    '--secret-id', 'carek9/ga4-service-account',
    '--region', 'us-east-2',
    '--query', 'SecretString',
    '--output', 'text'
]))

# Write temp credentials file
creds_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
json.dump(secret, creds_file)
creds_file.close()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = creds_file.name

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest, DateRange, Dimension, Metric, OrderBy
)

client = BetaAnalyticsDataClient()
PROPERTY = 'properties/523137923'
end = datetime.now()
start = end - timedelta(days=30)
date_range = DateRange(start_date=start.strftime('%Y-%m-%d'), end_date=end.strftime('%Y-%m-%d'))

def run_report(dimensions, metrics, limit=20):
    req = RunReportRequest(
        property=PROPERTY,
        date_ranges=[date_range],
        dimensions=[Dimension(name=d) for d in dimensions],
        metrics=[Metric(name=m) for m in metrics],
        limit=limit
    )
    resp = client.run_report(req)
    rows = []
    for row in resp.rows:
        r = {}
        for i, d in enumerate(dimensions):
            r[d] = row.dimension_values[i].value
        for i, m in enumerate(metrics):
            val = row.metric_values[i].value
            r[m] = float(val) if '.' in val else int(val)
        rows.append(r)
    return rows

def run_totals(metrics):
    req = RunReportRequest(
        property=PROPERTY,
        date_ranges=[date_range],
        metrics=[Metric(name=m) for m in metrics],
    )
    resp = client.run_report(req)
    result = {}
    if resp.rows:
        for i, m in enumerate(metrics):
            val = resp.rows[0].metric_values[i].value
            result[m] = float(val) if '.' in val else int(val)
    return result

print("Fetching totals...")
totals = run_totals(['sessions', 'activeUsers', 'screenPageViews', 'bounceRate', 'averageSessionDuration', 'engagedSessions'])

print("Fetching traffic sources...")
sources = run_report(['sessionDefaultChannelGroup'], ['sessions', 'activeUsers'], limit=10)

print("Fetching top pages...")
pages = run_report(['pagePath', 'pageTitle'], ['screenPageViews', 'activeUsers', 'averageSessionDuration'], limit=30)

print("Fetching devices...")
devices = run_report(['deviceCategory'], ['sessions', 'activeUsers'])

print("Fetching geography...")
geo = run_report(['country', 'region'], ['sessions', 'activeUsers'], limit=20)

print("Fetching daily trend...")
daily = run_report(['date'], ['sessions', 'activeUsers', 'screenPageViews'], limit=31)
daily.sort(key=lambda x: x['date'])

print("Fetching landing pages...")
landing = run_report(['landingPage'], ['sessions', 'bounceRate', 'averageSessionDuration'], limit=20)

print("Fetching referrers...")
referrers = run_report(['sessionSource'], ['sessions', 'activeUsers'], limit=15)

data = {
    "metadata": {
        "collectedAt": datetime.utcnow().isoformat() + "Z",
        "property": PROPERTY,
        "period": {
            "startDate": start.strftime('%Y-%m-%d'),
            "endDate": end.strftime('%Y-%m-%d'),
            "days": 30
        }
    },
    "totals": totals,
    "trafficSources": sources,
    "topPages": pages,
    "devices": devices,
    "geography": geo,
    "dailyTrend": daily,
    "landingPages": landing,
    "referrers": referrers
}

outdir = '/Users/zoelumos/.openclaw/workspace/zoe-dashboard/clients/carek9/ga4'
os.makedirs(outdir, exist_ok=True)
with open(os.path.join(outdir, 'data.json'), 'w') as f:
    json.dump(data, f, indent=2)

os.unlink(creds_file.name)
print(f"✅ GA4 data saved to {outdir}/data.json")
print(json.dumps(totals, indent=2))
