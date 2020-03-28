import urllib.request
import json
import time

def load_prometheus_query(query):
    req = urllib.request.Request(url=query)
    with urllib.request.urlopen(req) as f:
        return json.loads(f.read().decode('utf-8'))

def clean_trailing_slash(url):
    if url[-1] == '/':
        return url[:-1]
    return url

while True:
    time.sleep(5)
    instances = {}
    credits = {
        'INSTITUTION': set(),
        'COMPANY': set(),
        'PERSON': set(),
        'ASSOCIATION': set(),
    }

    jitsi_required_labels = [
        'instance',
        'jitsi_hosted_by',
        'jitsi_hosted_by_url'
        'jitsi_url'
        'jitsi_hosted_by_kind'
        'software'
        'available_bandwidth_mbps'
        'core_count'
    ]

    mm_required_labels = [
        'instance'
        'url'
        'hosted_by'
        'hosted_by_url'
        'hosted_by_kind'
        'available_bandwidth_mbps'
        'core_count'
        'software'
    ]

    participants_data = load_prometheus_query('http://prometheus:9090/api/v1/query?query=jitsi_participants')
    cpu_data = load_prometheus_query('http://prometheus:9090/api/v1/query?query=jitsi_cpu_usage')
    mm_data = load_prometheus_query('http://prometheus:9090/api/v1/query?query=probe_success{software="MM"}')

    for server in participants_data['data']['result']:
        if not all(key in server['metric'] for key in jitsi_required_labels):
            continue
        if server['metric']['software'] == 'JITSI':
            d = {}
            d['name'] = clean_trailing_slash(server['metric']['instance'].split(':')[0])
            d['user_count'] = int(server['value'][1])
            d['by'] = server['metric']['jitsi_hosted_by']
            d['by_url'] = clean_trailing_slash(server['metric']['jitsi_hosted_by_url'])
            d['url'] = clean_trailing_slash(server['metric']['jitsi_url'])
            d['by_kind'] = server['metric']['jitsi_hosted_by_kind']
            d['software'] = server['metric']['software']
            d['available_bandwidth_mbps'] = server['metric']['available_bandwidth_mbps']
            d['core_count'] = server['metric']['core_count']
            credits[d['by_kind']].add((d['by'], d['by_url']))
            instances[d['name']] = d
 
    for server in cpu_data['data']['result']:
        if not all(key in server['metric'] for key in jitsi_required_labels):
            continue
        if server['metric']['software'] == 'JITSI':
            name = clean_trailing_slash(server['metric']['instance'].split(':')[0])
            instances[name]['cpu_usage'] = round(float(server['value'][1]), ndigits=2)

    for server in mm_data['data']['result']:
        if not all(key in server['metric'] for key in mm_required_labels):
            continue
        if server['metric'].get('software') == 'MM' and server['value'][1] == '1':
            d = {}
            d['name'] = clean_trailing_slash(server['metric']['instance'].replace('https://', ''))
            d['url'] = clean_trailing_slash(server['metric']['url'])
            d['by'] = server['metric']['hosted_by']
            d['by_url'] = clean_trailing_slash(server['metric']['hosted_by_url'])
            d['by_kind'] = server['metric']['hosted_by_kind']
            d['software'] = server['metric']['software']
            d['available_bandwidth_mbps'] = server['metric']['available_bandwidth_mbps']
            d['core_count'] = server['metric']['core_count']
            credits[d['by_kind']].add((d['by'], d['by_url']))
            instances[d['name']] = d

    new_credits = {}
    for key, item in credits.items():
        new_credits[key] = list(item)

    result = {
        'instances': list(instances.values()),
        'credits': new_credits,
    }

    with open('/hosts.json', 'w') as f:
        f.write(json.dumps(result, indent=2))
