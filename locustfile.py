from locust import HttpUser, between, task
import random

class WebsiteUser(HttpUser):
    wait_time = between(3, 5)
    counter = 0
    stops = ["Ahmedabad", "Udaypur", "Jodhpur", "Jaipur", "Delhi", "Kanpur"]
    
    @task
    def search(self):
        frm = random.choice(self.stops)
        to = random.choice(self.stops)
        self.client.get(f"http://localhost:8000/api/v1/buses/search?date=22-07-2022&from={frm}&to={to}&page={random.randint(1, 5)}")
        # self.client.get(f"http://localhost:8000/api/v1/buses/search?date=22-07-2022&from={frm}&to={to}")

    # @task
    # def search(self):
    #     self.client.post("http://localhost:8000/api/v1/login", data={"email":"smit.patel@nickelfox.com", "password":"testuser"})

