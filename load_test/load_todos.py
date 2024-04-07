from math import log
from locust import HttpUser, task, between
from faker import Faker
import logging

fake = Faker()

class DjangoTodo(HttpUser):
    host = "http://localhost"
    fake = Faker()
    wait_time = between(1, 5)
            
    def fetch_csrf_token(self):
        if self.client.cookies.get("csrftoken"):
            self.client.headers.update({"X-CSRFToken": self.client.cookies["csrftoken"]})
        else:
            response = self.client.get("/api/user/get_csrf/")
            self.client.headers.update({"X-CSRFToken": response.text})
        print(f"CSRF token: {self.client.headers['X-CSRFToken']}")

    def create_user(self):
        self.fetch_csrf_token()
        username = self.fake.user_name()
        password = self.fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
        with self.client.post("/api/user/create_user/", json={"username": username, "password": password}, catch_response=True) as response:
            logging.info(f"Creating: {response.text}")
        # Put new cookie CSRF token in header
        self.fetch_csrf_token()
            
    def on_start(self):
        self.create_user()
    
    @task
    def create_todo_task(self):
        title = fake.sentence()
        description = fake.text()
        with self.client.post("/api/todo/create_todo/", json={"title": title, "description": description}, catch_response=True) as response:
            logging.info(f"Response: {response.text}")