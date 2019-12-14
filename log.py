class log:
    def __init__(self, id, timestamp, service, method, resource, status):
        self.id = id
        self.timestamp = timestamp
        self.service = service
        self.method = method
        self.resource = resource
        self.status = status
