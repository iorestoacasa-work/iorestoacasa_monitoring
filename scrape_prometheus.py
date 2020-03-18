import urllib.request
import json
import time

def load_prometheus_query(query):
    req = urllib.request.Request(url=query)
    with urllib.request.urlopen(req) as f:
        return json.loads(f.read().decode('utf-8'))

while True:
    time.sleep(5)
    instances = {}
    participants_data = load_prometheus_query('http://prometheus:9090/api/v1/query?query=jitsi_participants')
    cpu_data = load_prometheus_query('http://prometheus:9090/api/v1/query?query=jitsi_cpu_usage')

    for server in participants_data['data']['result']:
        if 'jitsi_hosted_by' in server['metric']:
            d = {}
            d['name'] = server['metric']['instance'].split(':')[0]
            d['user_count'] = int(server['value'][1])
            d['by'] = server['metric']['jitsi_hosted_by']
            d['by_url'] = server['metric']['jitsi_hosted_by_url']
            d['url'] = server['metric']['jitsi_url']
            instances[d['name']] = d
 
    for server in cpu_data['data']['result']:
        if 'jitsi_hosted_by' in server['metric']:
            name = server['metric']['instance'].split(':')[0]
            instances[name]['cpu_usage'] = round(float(server['value'][1]), ndigits=2)

    with open('/hosts.json', 'w') as f:
        f.write(json.dumps(list(instances.values()), indent=2))

