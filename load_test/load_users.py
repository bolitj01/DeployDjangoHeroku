from math import log
from locust import HttpUser, task, between
from faker import Faker
import logging

class DjangoUser(HttpUser):
    host = "http://localhost"
    fake = Faker()
    wait_time = between(1, 5)
            
    def fetch_csrf_token(self):
        response = self.client.get("/api/user/get_csrf/")
        self.client.headers.update({"X-CSRFToken": response.text})
        print(f"CSRF token: {response.text}")

    def create_user(self):
        self.fetch_csrf_token()
        username = self.fake.user_name()
        password = self.fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
        with self.client.post("/api/user/create_user/", json={"username": username, "password": password}, catch_response=True) as response:
            logging.info(f"Response: {response.text}")
            
    def logout_user(self):
        with self.client.get("/api/user/logout/") as response:
            logging.info(f"Response: {response.text}")
    
    @task
    def create_user_task(self):
        self.create_user()
        self.logout_user()
        
    
