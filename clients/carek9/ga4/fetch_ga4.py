#!/usr/bin/env python3
"""Fetch CareK9 GA4 data for the last 30 days."""

import json
import os
from datetime import datetime, timedelta
from google.oauth2 import service_account
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest,
    DateRange,
    Dimension,
    Metric,
)

# Service account credentials from AWS Secrets Manager
SERVICE_ACCOUNT_INFO = {
    "type": "service_account",
    "project_id": "maximal-backup-487205-h8",
    "private_key_id": "5adbcda094ac6f91a706ba049fdc187fd8201a06",
    "private_key": """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC1+i0jTGo3jAf1
Unmmhb0lUk60+KP6oyMeDsTwRuIdXmVcQjnvUZX/3trwNF5j33In49X29lFklZC3
nWMfOW6n5GDlTgq/E/aZBHyQ3t75j16I2aSYBK/A9cg/0b7nscgG7MH0oQEsezQr
Y8p7LNM6CVNjBdHqUGorIQ0BTlqtZCzwveH3vgivEwB3h8ykqsvwy6nNRrR0HOVh
VRWGOOJfAfD+CnoN222GdawyV6UVeYfHPEwZNSJYVyu0qiu5g8OILYoWRqfO+LBE
RgSxFca3jE626JqVX+ePwge6Gi1v0vAOn9vc5RGDAxPCYztbR2Y4/QFh0LHbi3qx
bImzHDxtAgMBAAECggEAGqLyziARIMNUUOI7IJb334l42tWAOconnu6I1iYnUnwu
4v5l+N6c0atUVGTzTLQiw1hT89u3Kz1smuvPMVKt8fukUTwx/NPBEex4XUOPfhZb
FItNo9t1Fw4C5eXfhzjcb2MNZYTW+qSoDL0vy1rS1O5o2xg5feOPvsi43MWUJp1B
U1x/dsC1WS66QxMHnCCSJs/HpoLvpUGqeJQsrhShBBvhGOR1up42UHjq2jbj23qA
oePlVZaKGSzZyCNI/9MYLUyQK7m3FyXuZkw7bzcvONozTH3ZAvLV2Tuc7VXpxnHQ
tNU6ZNQvpCsXbshWmgaeXBWjpYiMyMZkZfkT5j+RIwKBgQDnV6Mzims18YpXgpXg
e6vugp605ZWV9Maksg98hnM5f4mjzQWtl4yS/LxxmYep4NwN5CaKFG6ORjlcx1jS
nQi4ZMBKIjkFy7HKTv5cN2qBvjjQ9F3ki3X5AoyLhKeyCWhScEXNlYbm7pQz/09L
lCKHuZRIhnHoB7EMGPOHBTmFzwKBgQDJX5KZBs+xBld6Y7oCWa0Mvo/YRqGtP2su
pr3aloMPie3JxmeAD5D0JdIQwNcdEwZgzfUVQ3GRV89Qt7GYFGxZGgWwWXuuD51N
wQK+IN3A003kVWczNpGpl3UlbyuLzqW9gUz8lGD115RJNWMYukeXaHjTYz6GVBhr
mxj24ktlAwKBgQCmfI9avDbDr3xb1gJ+dwIYt6/3h3HLZUi/pdU3TJsHuh0X4KhB
cVsdPP1w04iqXMSAyrxhiqq1gRwvBNeLWq+34+nucAqRfTIJ4idzvf3MOVUyK2qW
2zafaZIzpdf5bIPDMEFL3lwjPXcypH4waf8fphJszzSSQ1bK2foIJV5sSQKBgE4X
gRtU9+AXrH7rA6x7qE9D6zadFX/BE0ixIvkM22CARbW0+lhAMR9tN0yF7CX7RcLu
u/d2AymxGtWblwR6DxZyr/gWi48RwRfxHKYsyrJHf3Jn6DCFHfHdqXFN7l42UjHu
XbOpuvw7kObfDEH/o1nFCu43E302SY4ZRJIhacmPAoGAMLWmVQd0GHyqU6Gr0lCc
5Cbz5+l4tflH3jUJWWYSiRU1BCITuCvWEYkfThSrArF7SGYLrsK+gGZnZUT8+TGq
sT2wVihqdYPgMHA6f5zWNuD2UEx5jL6A7YYezNSt8ifAtTGq6Hss2U9H4EHekAKA
purak4uL7f4eoMkQc/7xfzM=
-----END PRIVATE KEY-----
""",
    "client_email": "carek9-ga4-reader@maximal-backup-487205-h8.iam.gserviceaccount.com",
    "client_id": "109008951093395668202",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/carek9-ga4-reader%40maximal-backup-487205-h8.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

PROPERTY_ID = "523137923"

def get_client():
    """Create authenticated GA4 client."""
    credentials = service_account.Credentials.from_service_account_info(
        SERVICE_ACCOUNT_INFO,
        scopes=["https://www.googleapis.com/auth/analytics.readonly"]
    )
    return BetaAnalyticsDataClient(credentials=credentials)

def get_date_range():
    """Get date range for last 30 days."""
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)
    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")

def fetch_overview_metrics(client, start_date, end_date):
    """Fetch main metrics: sessions, users, pageviews, bounce rate."""
    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID}",
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        metrics=[
            Metric(name="sessions"),
            Metric(name="totalUsers"),
            Metric(name="screenPageViews"),
            Metric(name="bounceRate"),
            Metric(name="averageSessionDuration"),
            Metric(name="newUsers"),
        ]
    )
    response = client.run_report(request)
    
    if response.rows:
        row = response.rows[0]
        return {
            "sessions": int(row.metric_values[0].value),
            "totalUsers": int(row.metric_values[1].value),
            "pageviews": int(row.metric_values[2].value),
            "bounceRate": round(float(row.metric_values[3].value) * 100, 2),
            "avgSessionDuration": round(float(row.metric_values[4].value), 1),
            "newUsers": int(row.metric_values[5].value),
        }
    return {}

def fetch_top_pages(client, start_date, end_date, limit=10):
    """Fetch top pages by pageviews."""
    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID}",
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        dimensions=[Dimension(name="pagePath")],
        metrics=[
            Metric(name="screenPageViews"),
            Metric(name="sessions"),
        ],
        limit=limit
    )
    response = client.run_report(request)
    
    pages = []
    for row in response.rows:
        pages.append({
            "path": row.dimension_values[0].value,
            "pageviews": int(row.metric_values[0].value),
            "sessions": int(row.metric_values[1].value),
        })
    return pages

def fetch_traffic_sources(client, start_date, end_date, limit=10):
    """Fetch traffic sources by session source/medium."""
    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID}",
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        dimensions=[
            Dimension(name="sessionSource"),
            Dimension(name="sessionMedium"),
        ],
        metrics=[
            Metric(name="sessions"),
            Metric(name="totalUsers"),
        ],
        limit=limit
    )
    response = client.run_report(request)
    
    sources = []
    for row in response.rows:
        sources.append({
            "source": row.dimension_values[0].value,
            "medium": row.dimension_values[1].value,
            "sessions": int(row.metric_values[0].value),
            "users": int(row.metric_values[1].value),
        })
    return sources

def fetch_daily_trend(client, start_date, end_date):
    """Fetch daily sessions/users trend."""
    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID}",
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        dimensions=[Dimension(name="date")],
        metrics=[
            Metric(name="sessions"),
            Metric(name="totalUsers"),
            Metric(name="screenPageViews"),
        ],
    )
    response = client.run_report(request)
    
    daily = []
    for row in response.rows:
        daily.append({
            "date": row.dimension_values[0].value,
            "sessions": int(row.metric_values[0].value),
            "users": int(row.metric_values[1].value),
            "pageviews": int(row.metric_values[2].value),
        })
    # Sort by date
    daily.sort(key=lambda x: x["date"])
    return daily

def main():
    client = get_client()
    start_date, end_date = get_date_range()
    
    print(f"Fetching CareK9 GA4 data for {start_date} to {end_date}...")
    
    data = {
        "property_id": PROPERTY_ID,
        "date_range": {
            "start": start_date,
            "end": end_date,
        },
        "fetched_at": datetime.now().isoformat(),
        "overview": fetch_overview_metrics(client, start_date, end_date),
        "top_pages": fetch_top_pages(client, start_date, end_date),
        "traffic_sources": fetch_traffic_sources(client, start_date, end_date),
        "daily_trend": fetch_daily_trend(client, start_date, end_date),
    }
    
    # Save to JSON
    output_path = "/Users/zoelumos/.openclaw/workspace/zoe-dashboard/clients/carek9/ga4/data.json"
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"\nData saved to {output_path}")
    print("\n=== CareK9 GA4 Summary ===")
    print(f"Period: {start_date} to {end_date}")
    print(f"Sessions: {data['overview'].get('sessions', 'N/A'):,}")
    print(f"Users: {data['overview'].get('totalUsers', 'N/A'):,}")
    print(f"New Users: {data['overview'].get('newUsers', 'N/A'):,}")
    print(f"Pageviews: {data['overview'].get('pageviews', 'N/A'):,}")
    print(f"Bounce Rate: {data['overview'].get('bounceRate', 'N/A')}%")
    print(f"Avg Session Duration: {data['overview'].get('avgSessionDuration', 'N/A')}s")
    
    print("\nTop 5 Pages:")
    for i, page in enumerate(data['top_pages'][:5], 1):
        print(f"  {i}. {page['path']} - {page['pageviews']:,} views")
    
    print("\nTop 5 Traffic Sources:")
    for i, src in enumerate(data['traffic_sources'][:5], 1):
        print(f"  {i}. {src['source']}/{src['medium']} - {src['sessions']:,} sessions")

if __name__ == "__main__":
    main()
