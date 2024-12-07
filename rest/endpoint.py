import requests

class Endpoint:
    def __init__(self, path, name, get, put, post, delete, head):
        self.path = path
        self.name = name
        self.get = get
        self.put = put
        self.post = post
        self.delete = delete
        self.head = head

    def get_request(self, headers):
        return requests.get(self.path, headers=headers)

    def post_request(self, headers, data):
        return requests.post(self.path, headers=headers, data=data)

    def put_request(self, headers, data):
        return requests.put(self.path, headers=headers, data=data)

    def get_request(self, headers):
        return requests.get(self.path, headers=headers)

    def delete_request(self, headers):
        return requests.delete(self.path, headers=headers)

    def head_request(self, headers):
        return requests.head(self.path, headers=headers)

    def __str__(self):
        actions = ""
        if self.get:
            actions += "GET "
        if self.put:
            actions += "PUT "
        if self.post:
            actions += "POST "
        if self.delete:
            actions += "DELETE "
        if self.head:
            actions += "HEAD "
        return f"{self.name} ({self.path}) - {actions.strip()}"
