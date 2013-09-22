import json
import os.path

def fixture(name, raw=False):
    path = os.path.dirname(__file__)
    with open(os.path.join(path, 'fixtures', name)) as f:
        if not raw and name.endswith(".json"):
            return json.loads(f.read())
        else:
            return f.read()
