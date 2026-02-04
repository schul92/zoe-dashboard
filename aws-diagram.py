#!/usr/bin/env python3
"""
AWS Infrastructure Diagram Generator (Professional)
Uses the 'diagrams' library with official AWS icons
"""

import boto3
import os
from datetime import datetime

# Change to output directory
os.chdir('/home/ubuntu/.openclaw/workspace/dashboard')

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.security import SecretsManager
from diagrams.aws.integration import Eventbridge
from diagrams.aws.storage import S3
from diagrams.aws.network import VPC
from diagrams.aws.management import Cloudwatch

def get_aws_resources():
    """Fetch all relevant AWS resources"""
    resources = {
        'ec2': [],
        'lambda': [],
        'secrets': [],
        'eventbridge': [],
        'region': 'us-east-2'
    }
    
    region = 'us-east-2'
    
    # EC2 Instances
    try:
        ec2 = boto3.client('ec2', region_name=region)
        instances = ec2.describe_instances()
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                name = 'Unnamed'
                for tag in instance.get('Tags', []):
                    if tag['Key'] == 'Name':
                        name = tag['Value']
                resources['ec2'].append({
                    'id': instance['InstanceId'],
                    'name': name,
                    'state': instance['State']['Name'],
                    'type': instance['InstanceType']
                })
    except Exception as e:
        print(f"EC2 error: {e}")
    
    # Lambda Functions
    try:
        lam = boto3.client('lambda', region_name=region)
        functions = lam.list_functions()
        for fn in functions['Functions']:
            resources['lambda'].append({
                'name': fn['FunctionName'],
                'runtime': fn['Runtime'],
                'memory': fn['MemorySize']
            })
    except Exception as e:
        print(f"Lambda error: {e}")
    
    # Secrets Manager
    try:
        sm = boto3.client('secretsmanager', region_name=region)
        secrets = sm.list_secrets()
        for secret in secrets['SecretList']:
            resources['secrets'].append({
                'name': secret['Name'],
                'description': secret.get('Description', '')
            })
    except Exception as e:
        print(f"Secrets error: {e}")
    
    # EventBridge Rules
    try:
        events = boto3.client('events', region_name=region)
        rules = events.list_rules()
        for rule in rules['Rules']:
            # Get targets for this rule
            targets = events.list_targets_by_rule(Rule=rule['Name'])
            target_names = [t.get('Arn', '').split(':')[-1] for t in targets.get('Targets', [])]
            resources['eventbridge'].append({
                'name': rule['Name'],
                'schedule': rule.get('ScheduleExpression', 'event-based'),
                'state': rule['State'],
                'targets': target_names
            })
    except Exception as e:
        print(f"EventBridge error: {e}")
    
    return resources

def generate_diagram(resources):
    """Generate professional AWS diagram"""
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    with Diagram(
        "ZOE STUDIO - AWS Infrastructure",
        filename="aws-architecture",
        outformat="png",
        show=False,
        direction="TB",
        graph_attr={
            "fontsize": "20",
            "bgcolor": "white",
            "pad": "0.5",
            "splines": "spline",
        }
    ):
        
        with Cluster("AWS us-east-2"):
            
            # Secrets Manager
            with Cluster("Secrets Manager"):
                secrets = []
                for s in resources['secrets'][:5]:  # Limit to 5
                    secrets.append(SecretsManager(s['name'].replace('/', '\n')))
            
            # Lambda Functions
            with Cluster("Lambda Functions"):
                lambdas = {}
                for fn in resources['lambda']:
                    lambdas[fn['name']] = Lambda(f"{fn['name']}\n({fn['runtime']})")
            
            # EventBridge Rules
            with Cluster("EventBridge Schedules"):
                events = {}
                for rule in resources['eventbridge'][:5]:  # Limit to 5
                    schedule_short = rule['schedule'].replace('cron(', '').replace(')', '')[:15]
                    events[rule['name']] = Eventbridge(f"{rule['name'][:15]}\n{schedule_short}")
            
            # EC2 Instances
            if resources['ec2']:
                with Cluster("EC2 Instances"):
                    ec2s = {}
                    for inst in resources['ec2']:
                        status = "🟢" if inst['state'] == 'running' else "🔴"
                        ec2s[inst['id']] = EC2(f"{inst['name']}\n{inst['type']}\n{status}")
            
            # CloudWatch for monitoring
            cw = Cloudwatch("CloudWatch\nLogs & Metrics")
        
        # Draw connections
        # EventBridge -> Lambda
        for rule in resources['eventbridge']:
            rule_name = rule['name']
            if rule_name in events:
                for target in rule.get('targets', []):
                    # Match target to lambda
                    for lambda_name, lambda_node in lambdas.items():
                        if lambda_name.lower() in target.lower() or target.lower() in lambda_name.lower():
                            events[rule_name] >> Edge(color="orange", style="bold") >> lambda_node
        
        # Lambda -> Secrets (all lambdas read secrets)
        for lambda_node in lambdas.values():
            for secret in secrets[:1]:  # Just connect to first secret for clarity
                lambda_node >> Edge(color="red", style="dashed") >> secret
        
        # Lambda -> CloudWatch
        for lambda_node in lambdas.values():
            lambda_node >> Edge(color="blue", style="dotted") >> cw

def generate_html():
    """Generate HTML wrapper for the diagram"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZOE STUDIO AWS Infrastructure</title>
    <meta http-equiv="refresh" content="300"> <!-- Auto refresh every 5 min -->
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #232f3e 0%, #131920 100%);
            min-height: 100vh;
            color: #fff;
            padding: 20px;
        }}
        .container {{ max-width: 1600px; margin: 0 auto; }}
        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding: 20px;
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            border: 1px solid rgba(255,153,0,0.3);
        }}
        h1 {{ font-size: 1.8em; }}
        h1 span {{ color: #ff9900; }}
        .timestamp {{ color: #888; font-size: 0.9em; }}
        .diagram {{
            background: #fff;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }}
        .diagram img {{
            max-width: 100%;
            height: auto;
        }}
        .legend {{
            display: flex;
            gap: 20px;
            justify-content: center;
            margin-top: 20px;
            flex-wrap: wrap;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 16px;
            background: rgba(255,255,255,0.1);
            border-radius: 8px;
        }}
        .legend-color {{
            width: 20px;
            height: 4px;
            border-radius: 2px;
        }}
        .orange {{ background: #ff9900; }}
        .red {{ background: #dd344c; }}
        .blue {{ background: #3498db; }}
        .refresh-btn {{
            background: #ff9900;
            color: #000;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            text-decoration: none;
        }}
        .refresh-btn:hover {{ background: #ffad33; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div>
                <h1>🎯 <span>ZOE STUDIO</span> AWS Infrastructure</h1>
                <p class="timestamp">Last updated: {timestamp}</p>
                <p class="timestamp">Auto-refreshes every 5 minutes</p>
            </div>
            <a href="?" class="refresh-btn">🔄 Refresh Now</a>
        </header>
        
        <div class="diagram">
            <img src="aws-architecture.png?t={int(datetime.now().timestamp())}" alt="AWS Architecture Diagram">
        </div>
        
        <div class="legend">
            <div class="legend-item">
                <div class="legend-color orange"></div>
                <span>EventBridge → Lambda (triggers)</span>
            </div>
            <div class="legend-item">
                <div class="legend-color red"></div>
                <span>Lambda → Secrets (reads)</span>
            </div>
            <div class="legend-item">
                <div class="legend-color blue"></div>
                <span>Lambda → CloudWatch (logs)</span>
            </div>
        </div>
    </div>
</body>
</html>'''
    
    with open('/home/ubuntu/.openclaw/workspace/dashboard/index.html', 'w') as f:
        f.write(html)

def main():
    print("🔍 Fetching AWS resources...")
    resources = get_aws_resources()
    
    print(f"   Found: {len(resources['ec2'])} EC2, {len(resources['lambda'])} Lambda, {len(resources['secrets'])} Secrets, {len(resources['eventbridge'])} EventBridge rules")
    
    print("📊 Generating diagram...")
    generate_diagram(resources)
    
    print("🌐 Generating HTML...")
    generate_html()
    
    print("✅ Done! Dashboard updated.")

if __name__ == '__main__':
    main()
