#!/bin/bash
# Refresh SEO data from AWS Secrets Manager
# Run via cron: */30 * * * * /path/to/refresh.sh

cd "$(dirname "$0")"

# Get latest data from Secrets Manager
aws secretsmanager get-secret-value \
    --secret-id seo-data/kona-coffee \
    --region us-east-2 \
    --query 'SecretString' \
    --output text | jq '.' > data.json

echo "$(date): SEO data refreshed"
