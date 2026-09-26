import sys, requests, json
sys.stdout.reconfigure(encoding='utf-8')

url = 'http://127.0.0.1:8000/api/chat'
r1 = requests.post(url, json={
    'message': 'I want to automate my gpay transactions and track expenses in google sheets. Send me telegram notifications. Only for transactions above 500 rupees. Skip duplicates.',
    'thread_id': 'test_dynamic_icons_3'
}).json()

print('Status:', r1['status'])
print('Message:', r1['message'])
print()

wf = r1.get('workflow')
if not wf and r1['status'] == 'needs_clarification':
    r2 = requests.post(url, json={'message': 'yes', 'thread_id': 'test_dynamic_icons_3'}).json()
    print('Status:', r2['status'])
    wf = r2.get('workflow')

if wf:
    print('Workflow nodes:')
    for n in wf['nodes']:
        print(f"  {n['id']:15} type={n['type']:15} service={n.get('service','?'):20} label={n['label']}")
    print()
    print('Workflow edges:')
    for e in wf['edges']:
        print(f"  {e['source']:15} -> {e['target']:15} label={e.get('label','')}")
