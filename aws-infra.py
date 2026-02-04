#!/usr/bin/env python3
"""
AWS Infrastructure Diagram Generator
Generates a Mermaid diagram of your AWS resources
"""

import boto3
import json
from datetime import datetime

def get_aws_resources():
    """Fetch all relevant AWS resources"""
    resources = {
        'ec2': [],
        'lambda': [],
        'secrets': [],
        'eventbridge': [],
        's3': [],
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
            resources['eventbridge'].append({
                'name': rule['Name'],
                'schedule': rule.get('ScheduleExpression', 'event-based'),
                'state': rule['State']
            })
    except Exception as e:
        print(f"EventBridge error: {e}")
    
    # S3 Buckets (global, but filter by region if possible)
    try:
        s3 = boto3.client('s3', region_name=region)
        buckets = s3.list_buckets()
        for bucket in buckets.get('Buckets', []):
            resources['s3'].append({
                'name': bucket['Name']
            })
    except Exception as e:
        pass  # Might not have S3 access
    
    return resources

def generate_mermaid(resources):
    """Generate Mermaid diagram from resources"""
    lines = ['flowchart TB']
    lines.append('    subgraph AWS["☁️ AWS us-east-2"]')
    
    # EC2 Section
    if resources['ec2']:
        lines.append('        subgraph EC2["🖥️ EC2 Instances"]')
        for i, ec2 in enumerate(resources['ec2']):
            state_icon = '🟢' if ec2['state'] == 'running' else '🔴'
            lines.append(f'            ec2_{i}["{state_icon} {ec2["name"]}<br/>{ec2["type"]}"]')
        lines.append('        end')
    
    # Lambda Section
    if resources['lambda']:
        lines.append('        subgraph Lambda["⚡ Lambda Functions"]')
        for i, fn in enumerate(resources['lambda']):
            lines.append(f'            lambda_{i}["{fn["name"]}<br/>🐍 {fn["runtime"]}"]')
        lines.append('        end')
    
    # Secrets Section
    if resources['secrets']:
        lines.append('        subgraph Secrets["🔐 Secrets Manager"]')
        for i, secret in enumerate(resources['secrets']):
            lines.append(f'            secret_{i}["{secret["name"]}"]')
        lines.append('        end')
    
    # EventBridge Section
    if resources['eventbridge']:
        lines.append('        subgraph Events["⏰ EventBridge"]')
        for i, rule in enumerate(resources['eventbridge']):
            state_icon = '🟢' if rule['state'] == 'ENABLED' else '🔴'
            lines.append(f'            event_{i}["{state_icon} {rule["name"]}"]')
        lines.append('        end')
    
    lines.append('    end')
    
    # Connections
    lines.append('')
    lines.append('    %% Connections')
    
    # EventBridge -> Lambda
    for i, rule in enumerate(resources['eventbridge']):
        for j, fn in enumerate(resources['lambda']):
            if fn['name'].lower() in rule['name'].lower() or rule['name'].lower() in fn['name'].lower():
                lines.append(f'    event_{i} -->|triggers| lambda_{j}')
    
    # Lambda -> Secrets
    for i, fn in enumerate(resources['lambda']):
        for j, secret in enumerate(resources['secrets']):
            if 'kona' in fn['name'].lower() and 'kona' in secret['name'].lower():
                lines.append(f'    lambda_{i} -.->|reads| secret_{j}')
    
    # Styling
    lines.append('')
    lines.append('    %% Styling')
    lines.append('    classDef running fill:#d4edda,stroke:#28a745')
    lines.append('    classDef stopped fill:#f8d7da,stroke:#dc3545')
    lines.append('    classDef lambda fill:#ff9900,stroke:#cc7a00,color:#fff')
    lines.append('    classDef secret fill:#dd344c,stroke:#aa2238,color:#fff')
    
    return '\n'.join(lines)

def generate_html(mermaid_code, resources):
    """Generate HTML page with the diagram"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
    
    # Stats
    stats = {
        'ec2': len(resources['ec2']),
        'lambda': len(resources['lambda']),
        'secrets': len(resources['secrets']),
        'eventbridge': len(resources['eventbridge'])
    }
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZOE STUDIO AWS Infrastructure</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            color: #fff;
            padding: 20px;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding: 20px;
            background: rgba(255,255,255,0.1);
            border-radius: 12px;
            backdrop-filter: blur(10px);
        }}
        h1 {{ font-size: 1.8em; }}
        h1 span {{ color: #ff9900; }}
        .timestamp {{ color: #888; font-size: 0.9em; }}
        .stats {{
            display: flex;
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat {{
            background: rgba(255,255,255,0.1);
            padding: 20px 30px;
            border-radius: 12px;
            text-align: center;
            backdrop-filter: blur(10px);
        }}
        .stat-value {{ font-size: 2em; font-weight: bold; color: #ff9900; }}
        .stat-label {{ color: #888; margin-top: 5px; }}
        .diagram {{
            background: #fff;
            border-radius: 12px;
            padding: 30px;
            overflow-x: auto;
        }}
        .mermaid {{ text-align: center; }}
        .refresh-btn {{
            background: #ff9900;
            color: #000;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
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
            </div>
            <button class="refresh-btn" onclick="location.reload()">🔄 Refresh</button>
        </header>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-value">{stats['ec2']}</div>
                <div class="stat-label">🖥️ EC2 Instances</div>
            </div>
            <div class="stat">
                <div class="stat-value">{stats['lambda']}</div>
                <div class="stat-label">⚡ Lambda Functions</div>
            </div>
            <div class="stat">
                <div class="stat-value">{stats['secrets']}</div>
                <div class="stat-label">🔐 Secrets</div>
            </div>
            <div class="stat">
                <div class="stat-value">{stats['eventbridge']}</div>
                <div class="stat-label">⏰ Scheduled Rules</div>
            </div>
        </div>
        
        <div class="diagram">
            <pre class="mermaid">
{mermaid_code}
            </pre>
        </div>
    </div>
    
    <script>
        mermaid.initialize({{ 
            startOnLoad: true,
            theme: 'default',
            flowchart: {{ 
                useMaxWidth: true,
                htmlLabels: true,
                curve: 'basis'
            }}
        }});
    </script>
</body>
</html>'''
    return html

def main():
    print("🔍 Fetching AWS resources...")
    resources = get_aws_resources()
    
    print("📊 Generating diagram...")
    mermaid = generate_mermaid(resources)
    html = generate_html(mermaid, resources)
    
    output_path = '/home/ubuntu/.openclaw/workspace/dashboard/index.html'
    with open(output_path, 'w') as f:
        f.write(html)
    
    print(f"✅ Dashboard generated: {output_path}")
    print(f"   EC2: {len(resources['ec2'])}")
    print(f"   Lambda: {len(resources['lambda'])}")
    print(f"   Secrets: {len(resources['secrets'])}")
    print(f"   EventBridge: {len(resources['eventbridge'])}")

if __name__ == '__main__':
    main()
