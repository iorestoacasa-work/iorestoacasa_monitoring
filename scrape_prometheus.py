import urllib.request
import json
import time

while True:
    time.sleep(5)
    instances = []
    req = urllib.request.Request(url='http://prometheus:9090/api/v1/query?query=jitsi_participants')
    with urllib.request.urlopen(req) as f:
        data = json.loads(f.read().decode('utf-8'))

    for server in data['data']['result']:
        if 'jitsi_hosted_by' in server['metric']:
            d = {}
            d['name'] = server['metric']['instance'].split(':')[0]
            d['user_count'] = server['value'][1]
            d['by'] = server['metric']['jitsi_hosted_by']
            d['by_url'] = server['metric']['jitsi_hosted_by_url']
            d['url'] = server['metric']['jitsi_url']
            instances.append(d)

    with open('/hosts.json', 'w') as f:
        f.write(json.dumps(instances, indent=2))

