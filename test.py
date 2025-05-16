import json

record_file = "__REC__1701990221786663.json"
with open(record_file, 'r') as f:
    data = json.load(f)

print(data[-1])