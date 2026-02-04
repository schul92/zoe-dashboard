#!/usr/bin/env python3
"""
AWS Infrastructure Diagram - Auto-Scaling Edition
Dynamically fetches ALL AWS resources and generates diagram
Scales automatically as infrastructure grows
"""

import boto3
import os
from datetime import datetime
from collections import defaultdict

os.chdir('/home/ubuntu/.openclaw/workspace/dashboard')

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.security import SecretsManager
from diagrams.aws.integration import Eventbridge
from diagrams.aws.management import Cloudwatch
from diagrams.aws.general import Users
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.storage import S3
from diagrams.aws.network import APIGateway, ELB, CloudFront
from diagrams.aws.analytics import Athena, Kinesis
from diagrams.aws.ml import Sagemaker

REGION = 'us-east-2'

def fetch_all_resources():
    """Dynamically fetch ALL AWS resources"""
    resources = defaultdict(list)
    
    # EC2 Instances
    try:
        ec2 = boto3.client('ec2', region_name=REGION)
        for res in ec2.describe_instances()['Reservations']:
            for inst in res['Instances']:
                # Skip terminated instances
                if inst['State']['Name'] == 'terminated':
                    continue
                name = next((t['Value'] for t in inst.get('Tags', []) if t['Key'] == 'Name'), inst['InstanceId'][:12])
                resources['ec2'].append({
                    'id': inst['InstanceId'],
                    'name': name,
                    'type': inst['InstanceType'],
                    'state': inst['State']['Name']
                })
    except Exception as e:
        print(f"  EC2: {e}")
    
    # Lambda Functions
    try:
        lam = boto3.client('lambda', region_name=REGION)
        paginator = lam.get_paginator('list_functions')
        for page in paginator.paginate():
            for fn in page['Functions']:
                resources['lambda'].append({
                    'name': fn['FunctionName'],
                    'runtime': fn.get('Runtime', 'N/A'),
                    'memory': fn.get('MemorySize', 128)
                })
    except Exception as e:
        print(f"  Lambda: {e}")
    
    # Secrets Manager
    try:
        sm = boto3.client('secretsmanager', region_name=REGION)
        paginator = sm.get_paginator('list_secrets')
        for page in paginator.paginate():
            for secret in page['SecretList']:
                resources['secrets'].append({
                    'name': secret['Name'],
                    'arn': secret['ARN']
                })
    except Exception as e:
        print(f"  Secrets: {e}")
    
    # EventBridge Rules
    try:
        events = boto3.client('events', region_name=REGION)
        rules = events.list_rules()
        for rule in rules.get('Rules', []):
            targets = []
            try:
                t = events.list_targets_by_rule(Rule=rule['Name'])
                targets = [x.get('Arn', '').split(':')[-1] for x in t.get('Targets', [])]
            except:
                pass
            resources['eventbridge'].append({
                'name': rule['Name'],
                'schedule': rule.get('ScheduleExpression', 'event'),
                'state': rule['State'],
                'targets': targets
            })
    except Exception as e:
        print(f"  EventBridge: {e}")
    
    # S3 Buckets
    try:
        s3 = boto3.client('s3', region_name=REGION)
        for bucket in s3.list_buckets().get('Buckets', []):
            resources['s3'].append({'name': bucket['Name']})
    except Exception as e:
        print(f"  S3: {e}")
    
    # RDS Instances
    try:
        rds = boto3.client('rds', region_name=REGION)
        for db in rds.describe_db_instances().get('DBInstances', []):
            resources['rds'].append({
                'name': db['DBInstanceIdentifier'],
                'engine': db['Engine'],
                'status': db['DBInstanceStatus']
            })
    except Exception as e:
        print(f"  RDS: {e}")
    
    # DynamoDB Tables
    try:
        ddb = boto3.client('dynamodb', region_name=REGION)
        for table in ddb.list_tables().get('TableNames', []):
            resources['dynamodb'].append({'name': table})
    except Exception as e:
        print(f"  DynamoDB: {e}")
    
    # API Gateway
    try:
        apigw = boto3.client('apigateway', region_name=REGION)
        for api in apigw.get_rest_apis().get('items', []):
            resources['apigateway'].append({'name': api['name'], 'id': api['id']})
    except Exception as e:
        print(f"  API Gateway: {e}")
    
    # Load Balancers
    try:
        elbv2 = boto3.client('elbv2', region_name=REGION)
        for lb in elbv2.describe_load_balancers().get('LoadBalancers', []):
            resources['elb'].append({'name': lb['LoadBalancerName'], 'type': lb['Type']})
    except Exception as e:
        print(f"  ELB: {e}")
    
    # CloudFront Distributions
    try:
        cf = boto3.client('cloudfront')
        for dist in cf.list_distributions().get('DistributionList', {}).get('Items', []):
            resources['cloudfront'].append({'id': dist['Id'], 'domain': dist['DomainName']})
    except Exception as e:
        print(f"  CloudFront: {e}")
    
    return resources

def generate_diagram(resources):
    """Generate scalable diagram based on discovered resources"""
    
    # Calculate DPI based on total resources (smaller if more resources)
    total = sum(len(v) for v in resources.values())
    dpi = "100" if total > 20 else "120" if total > 10 else "150"
    
    with Diagram(
        "",
        filename="aws-architecture",
        outformat="png",
        show=False,
        direction="TB",  # Top to bottom for scalability
        graph_attr={
            "dpi": dpi,
            "pad": "0.5",
            "nodesep": "0.3",
            "ranksep": "0.5",
            "fontsize": "10",
            "bgcolor": "white",
        },
        node_attr={
            "fontsize": "8",
            "width": "0.9",
            "height": "0.9",
        },
    ):
        # External Users
        telegram = Users("Telegram")
        
        with Cluster(f"AWS Cloud ({REGION})", graph_attr={"fontsize": "10", "bgcolor": "#f5f5f5"}):
            
            # ---- SCHEDULING TIER ----
            eb_nodes = []
            if resources['eventbridge']:
                with Cluster(f"EventBridge ({len(resources['eventbridge'])} rules)", graph_attr={"fontsize": "9", "bgcolor": "#FFF3E0"}):
                    for rule in resources['eventbridge']:
                        short_name = rule['name'][:12] + ('...' if len(rule['name']) > 12 else '')
                        eb_nodes.append(Eventbridge(short_name))
            
            # ---- COMPUTE TIER ----
            lambda_nodes = {}
            if resources['lambda']:
                with Cluster(f"Lambda ({len(resources['lambda'])} functions)", graph_attr={"fontsize": "9", "bgcolor": "#E3F2FD"}):
                    for fn in resources['lambda']:
                        short_name = fn['name'][:14] + ('...' if len(fn['name']) > 14 else '')
                        lambda_nodes[fn['name']] = Lambda(short_name)
            
            ec2_nodes = {}
            if resources['ec2']:
                with Cluster(f"EC2 ({len(resources['ec2'])} instances)", graph_attr={"fontsize": "9", "bgcolor": "#E8F5E9"}):
                    for inst in resources['ec2']:
                        status = "🟢" if inst['state'] == 'running' else "🔴"
                        label = f"{inst['name'][:10]}\n{status}"
                        ec2_nodes[inst['id']] = EC2(label)
            
            # ---- DATA TIER ----
            secret_nodes = []
            if resources['secrets']:
                with Cluster(f"Secrets ({len(resources['secrets'])})", graph_attr={"fontsize": "9", "bgcolor": "#FCE4EC"}):
                    for s in resources['secrets']:
                        short_name = s['name'].split('/')[-1][:12]
                        secret_nodes.append(SecretsManager(short_name))
            
            db_nodes = []
            if resources['rds']:
                with Cluster(f"RDS ({len(resources['rds'])})", graph_attr={"fontsize": "9", "bgcolor": "#E1F5FE"}):
                    for db in resources['rds']:
                        db_nodes.append(RDS(db['name'][:12]))
            
            if resources['dynamodb']:
                with Cluster(f"DynamoDB ({len(resources['dynamodb'])})", graph_attr={"fontsize": "9", "bgcolor": "#FFF8E1"}):
                    for table in resources['dynamodb']:
                        db_nodes.append(Dynamodb(table['name'][:12]))
            
            # ---- STORAGE TIER ----
            s3_nodes = []
            if resources['s3']:
                with Cluster(f"S3 ({len(resources['s3'])} buckets)", graph_attr={"fontsize": "9", "bgcolor": "#F3E5F5"}):
                    for bucket in resources['s3'][:5]:  # Limit to 5 for readability
                        s3_nodes.append(S3(bucket['name'][:12]))
                    if len(resources['s3']) > 5:
                        s3_nodes.append(S3(f"+{len(resources['s3'])-5} more"))
            
            # ---- NETWORK TIER ----
            api_nodes = []
            if resources['apigateway']:
                with Cluster(f"API Gateway ({len(resources['apigateway'])})", graph_attr={"fontsize": "9", "bgcolor": "#E0F2F1"}):
                    for api in resources['apigateway']:
                        api_nodes.append(APIGateway(api['name'][:12]))
            
            if resources['elb']:
                with Cluster(f"Load Balancers ({len(resources['elb'])})", graph_attr={"fontsize": "9", "bgcolor": "#ECEFF1"}):
                    for lb in resources['elb']:
                        ELB(lb['name'][:12])
            
            # CloudWatch (always present)
            cw = Cloudwatch("CloudWatch")
        
        # External services
        social = Users("Social APIs")
        
        # ---- CONNECTIONS ----
        # EventBridge → Lambda
        for i, eb in enumerate(eb_nodes):
            if i < len(lambda_nodes):
                target_lambda = list(lambda_nodes.values())[i % len(lambda_nodes)]
                eb >> Edge(color="#FF9900") >> target_lambda
        
        # Telegram → EC2 (Zoe)
        if ec2_nodes:
            first_ec2 = list(ec2_nodes.values())[0]
            telegram >> Edge(color="#0088cc", style="bold") >> first_ec2
        
        # Lambda → Secrets
        if secret_nodes and lambda_nodes:
            main_secret = secret_nodes[0]
            for lam in lambda_nodes.values():
                lam >> Edge(color="#DD344C", style="dashed") >> main_secret
        
        # Lambda → Social APIs
        for lam in list(lambda_nodes.values())[:2]:
            lam >> Edge(color="#3F8624") >> social
        
        # Lambda → CloudWatch
        for lam in lambda_nodes.values():
            lam >> Edge(color="#7B68EE", style="dotted") >> cw

def generate_html(resources):
    """Generate dashboard HTML"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
    
    # Build stats dynamically
    stats = [
        ('EventBridge', len(resources['eventbridge']), '#FF9900'),
        ('Lambda', len(resources['lambda']), '#FF9900'),
        ('EC2', len(resources['ec2']), '#FF9900'),
        ('Secrets', len(resources['secrets']), '#DD344C'),
        ('S3', len(resources['s3']), '#3F8624'),
        ('RDS', len(resources['rds']), '#3B48CC'),
        ('DynamoDB', len(resources['dynamodb']), '#4053D6'),
        ('API GW', len(resources['apigateway']), '#A166FF'),
        ('ELB', len(resources['elb']), '#8C4FFF'),
    ]
    
    # Filter out empty stats
    stats = [(n, v, c) for n, v, c in stats if v > 0]
    
    stats_html = ''.join([
        f'<div class="stat"><div class="stat-value" style="color:{c}">{v}</div><div class="stat-label">{n}</div></div>'
        for n, v, c in stats
    ])
    
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ZOE STUDIO AWS Architecture</title>
    <meta http-equiv="refresh" content="300">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, sans-serif; background: #0d1117; color: #c9d1d9; min-height: 100vh; }}
        .header {{ background: #161b22; padding: 16px 24px; border-bottom: 1px solid #30363d; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; }}
        .logo {{ font-size: 18px; font-weight: 600; color: #f0f6fc; }}
        .logo span {{ color: #FF9900; }}
        .meta {{ font-size: 12px; color: #8b949e; text-align: right; }}
        .main {{ max-width: 1400px; margin: 24px auto; padding: 0 24px; }}
        .stats {{ display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 24px; justify-content: center; }}
        .stat {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 14px 20px; text-align: center; min-width: 100px; }}
        .stat-value {{ font-size: 24px; font-weight: 700; }}
        .stat-label {{ font-size: 10px; color: #8b949e; margin-top: 4px; }}
        .diagram {{ background: #fff; border-radius: 8px; padding: 20px; text-align: center; overflow-x: auto; }}
        .diagram img {{ max-width: 100%; height: auto; }}
        .legend {{ display: flex; gap: 16px; justify-content: center; margin-top: 16px; font-size: 11px; color: #8b949e; flex-wrap: wrap; }}
        .legend span {{ display: flex; align-items: center; gap: 6px; }}
        .dot {{ width: 14px; height: 3px; border-radius: 2px; }}
        .footer {{ text-align: center; margin-top: 24px; font-size: 11px; color: #484f58; }}
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">🎯 <span>ZOE STUDIO</span> AWS Architecture</div>
        <div class="meta">
            <div>Last scan: {timestamp}</div>
            <div>Region: {REGION} • Auto-updates every 5 min</div>
        </div>
    </div>
    <div class="main">
        <div class="stats">{stats_html}</div>
        <div class="diagram">
            <img src="aws-architecture.png?t={int(datetime.now().timestamp())}" alt="AWS Architecture">
        </div>
        <div class="legend">
            <span><div class="dot" style="background:#FF9900"></div> Triggers</span>
            <span><div class="dot" style="background:#0088cc"></div> Users</span>
            <span><div class="dot" style="background:#DD344C"></div> Secrets</span>
            <span><div class="dot" style="background:#3F8624"></div> APIs</span>
            <span><div class="dot" style="background:#7B68EE"></div> Logs</span>
        </div>
    </div>
    <div class="footer">Auto-generated • Scales dynamically as infrastructure grows</div>
</body>
</html>'''
    
    with open('index.html', 'w') as f:
        f.write(html)

def main():
    print(f"🔍 Scanning AWS resources in {REGION}...")
    resources = fetch_all_resources()
    
    total = sum(len(v) for v in resources.values())
    print(f"📊 Found {total} total resources:")
    for k, v in resources.items():
        if v:
            print(f"   • {k}: {len(v)}")
    
    print("🎨 Generating scalable diagram...")
    generate_diagram(resources)
    
    print("🌐 Updating dashboard...")
    generate_html(resources)
    
    print("✅ Done!")

if __name__ == '__main__':
    main()
