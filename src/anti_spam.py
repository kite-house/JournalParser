from datetime import datetime



DELAY = 20
requests = {}

def timeout(id):
    if id in tuple(requests.keys()) and datetime.now().timestamp() - requests[id] < 20:
        return False
        
    requests[id] = datetime.now().timestamp()
    return True
