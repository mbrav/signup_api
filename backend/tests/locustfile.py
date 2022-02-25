import random
import string

from locust import HttpUser, task


def random_lower_string(num: int = 20) -> str:
    return ''.join(random.choices(string.ascii_lowercase, k=num))


def random_numbers(num: int = 20) -> str:
    return ''.join(random.choices(string.digits, k=num))


def random_id_string(num: int = 20) -> str:
    return ''.join(random.choices(string.ascii_letters, k=num))


def random_email() -> str:
    return f'{random_lower_string(10)}@{random_lower_string(5)}.com'


def random_phone(num: int = 20) -> str:
    return '+' + random_numbers(11)


class TestLocust(HttpUser):

    @task
    def index_page(self):
        self.client.get('/api/')

    @task
    def generate_signup(self):
        new_signup = {
            'first_name': random_lower_string(10).capitalize(),
            'last_name': random_lower_string(12).capitalize(),
            'phone': random_phone(),
            'email': random_email(),
            'class_id': random_id_string(20),
        }
        self.client.post('/api/signups', json=new_signup)

    @task
    def retrieve_signup(self):
        self.client.get('/api/signups/1')
