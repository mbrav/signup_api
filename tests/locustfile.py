from locust import HttpUser, task


class TestAPI(HttpUser):

    @task
    def index_page(self):
        self.client.get('/')

    @task
    def generate_signup(self):
        new_signup = {
            "first_name": "John",
            "last_name": "Appleseed",
            "phone": "+19171113434",
            "email": "john@apple.com",
            "class_id": "234234234",
            "date_created": "today"
        }
        self.client.post('/signup', json=new_signup)

    @task
    def retrieve_signup(self):
        self.client.get('/signup/1')
