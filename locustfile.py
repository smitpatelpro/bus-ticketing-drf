from locust import HttpUser, between, task
import random

class WebsiteUser(HttpUser):
    '''
    This is used to simulate search requests and measure performance.
    '''
    wait_time = between(3, 5)
    counter = 0
    stops = ["Ahmedabad", "Udaypur", "Jodhpur", "Jaipur", "Delhi", "Kanpur"]
    
    @task
    def search(self):
        frm = random.choice(self.stops)
        to = random.choice(self.stops)
        self.client.get(f"http://localhost:8000/api/v1/buses/search?date=22-07-2022&from={frm}&to={to}")
