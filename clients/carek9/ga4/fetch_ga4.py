#!/usr/bin/env python3
"""Fetch GA4 data for CareK9 using service account authentication."""

import json
import time
import jwt
import requests
from datetime import datetime, timedelta

# Service account credentials
SERVICE_ACCOUNT = {
    "client_email": "carek9-ga4-reader@maximal-backup-487205-h8.iam.gserviceaccount.com",
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
    "token_uri": "https://oauth2.googleapis.com/token"
}

PROPERTY_ID = "523137923"
GA4_API_BASE = "https://analyticsdata.googleapis.com/v1beta"


def get_access_token():
    """Generate JWT and exchange for access token."""
    now = int(time.time())
    payload = {
        "iss": SERVICE_ACCOUNT["client_email"],
        "sub": SERVICE_ACCOUNT["client_email"],
        "aud": SERVICE_ACCOUNT["token_uri"],
        "iat": now,
        "exp": now + 3600,
        "scope": "https://www.googleapis.com/auth/analytics.readonly"
    }
    
    signed_jwt = jwt.encode(payload, SERVICE_ACCOUNT["private_key"], algorithm="RS256")
    
    response = requests.post(
        SERVICE_ACCOUNT["token_uri"],
        data={
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": signed_jwt
        }
    )
    response.raise_for_status()
    return response.json()["access_token"]


def run_report(access_token, dimensions, metrics, limit=10):
    """Run a GA4 report."""
    url = f"{GA4_API_BASE}/properties/{PROPERTY_ID}:runReport"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Last 30 days
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    body = {
        "dateRanges": [{"startDate": start_date, "endDate": end_date}],
        "dimensions": [{"name": d} for d in dimensions] if dimensions else [],
        "metrics": [{"name": m} for m in metrics],
        "limit": limit
    }
    
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()


def extract_totals(report):
    """Extract metric totals from a report."""
    totals = {}
    if "rows" in report and report["rows"]:
        for i, metric in enumerate(report.get("metricHeaders", [])):
            name = metric["name"]
            value = report["rows"][0]["metricValues"][i]["value"]
            totals[name] = float(value) if "." in value else int(value)
    return totals


def extract_dimension_data(report, dim_name):
    """Extract dimension breakdown from a report."""
    results = []
    if "rows" in report:
        for row in report["rows"]:
            item = {dim_name: row["dimensionValues"][0]["value"]}
            for i, metric in enumerate(report.get("metricHeaders", [])):
                value = row["metricValues"][i]["value"]
                item[metric["name"]] = float(value) if "." in value else int(value)
            results.append(item)
    return results


def main():
    print("Authenticating with GA4...")
    access_token = get_access_token()
    print("✓ Authenticated")
    
    # Fetch overall metrics
    print("Fetching overall metrics...")
    overall_report = run_report(
        access_token,
        dimensions=[],
        metrics=["sessions", "totalUsers", "screenPageViews", "bounceRate"]
    )
    overall = extract_totals(overall_report)
    
    # Fetch top pages
    print("Fetching top pages...")
    pages_report = run_report(
        access_token,
        dimensions=["pagePath"],
        metrics=["screenPageViews", "sessions"],
        limit=10
    )
    top_pages = extract_dimension_data(pages_report, "pagePath")
    
    # Fetch traffic sources
    print("Fetching traffic sources...")
    sources_report = run_report(
        access_token,
        dimensions=["sessionSource"],
        metrics=["sessions", "totalUsers"],
        limit=10
    )
    traffic_sources = extract_dimension_data(sources_report, "sessionSource")
    
    # Compile results
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    data = {
        "property_id": PROPERTY_ID,
        "date_range": {
            "start": start_date,
            "end": end_date
        },
        "fetched_at": datetime.now().isoformat(),
        "metrics": {
            "sessions": overall.get("sessions", 0),
            "users": overall.get("totalUsers", 0),
            "pageviews": overall.get("screenPageViews", 0),
            "bounce_rate": round(overall.get("bounceRate", 0) * 100, 2)
        },
        "top_pages": top_pages,
        "traffic_sources": traffic_sources
    }
    
    # Save to JSON
    output_path = "/Users/zoelumos/.openclaw/workspace/zoe-dashboard/clients/carek9/ga4/data.json"
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"✓ Data saved to {output_path}")
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
