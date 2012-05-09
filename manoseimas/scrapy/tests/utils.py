import os.path


def fixture(name):
    path = os.path.dirname(__file__)
    with open(os.path.join(path, 'fixtures', name)) as f:
        return f.read()
