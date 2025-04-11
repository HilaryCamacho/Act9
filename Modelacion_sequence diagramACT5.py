import random
import time
from typing import Optional, Dict, Tuple, List

class User:
    def __init__(self, user_id: int, name: str, location: Tuple[float, float]):
        self.user_id = user_id
        self.name = name
        self.location = location  # (latitude, longitude)
        self.current_request: Optional[ServiceRequest] = None

    def submit_request(self, problem_details: str, system) -> Optional['ServiceRequest']:
        print(f"\n{self.name} is submitting a request: '{problem_details}'")
        self.current_request = system.process_request(self, problem_details, self.location)
        return self.current_request

    def view_provider_details(self) -> None:
        if self.current_request and self.current_request.provider:
            provider = self.current_request.provider
            print(f"\nProvider details for {self.name}:")
            print(f"Name: {provider.name}")
            print(f"ID: {provider.provider_id}")
            print(f"Current location: {provider.location}")
        else:
            print("No provider assigned to current request")

    def track_provider(self) -> None:
        if self.current_request and self.current_request.provider:
            print(f"\n{self.name} is tracking {self.current_request.provider.name}'s location in real-time:")
            # Simulate location updates every 2 seconds
            for i in range(3):
                new_location = (
                    self.current_request.provider.location[0] + random.uniform(-0.01, 0.01),
                    self.current_request.provider.location[1] + random.uniform(-0.01, 0.01)
                )
                self.current_request.provider.update_location(new_location)
                print(f"Update {i+1}: Provider is now at {new_location}")
                time.sleep(2)
        else:
            print("No provider assigned to track")

    def confirm_completion(self) -> bool:
        if self.current_request and self.current_request.status == "completed":
            print(f"\n{self.name} confirms service completion")
            # Payment would be processed here in a real system
            print("Payment processed successfully")
            return True
        print("Cannot confirm completion - service not marked as complete")
        return False

    def submit_review(self, rating: int, comment: str) -> bool:
        if self.current_request and self.current_request.status == "completed":
            print(f"\n{self.name} is submitting a review: {rating} stars - '{comment}'")
            self.current_request.add_review(rating, comment)
            return True
        print("Cannot submit review - service not completed")
        return False


class Provider:
    def __init__(self, provider_id: int, name: str, location: Tuple[float, float]):
        self.provider_id = provider_id
        self.name = name
        self.location = location
        self.available = True
        self.current_request: Optional[ServiceRequest] = None

    def update_location(self, new_location: Tuple[float, float]) -> None:
        self.location = new_location

    def confirm_request(self, request: 'ServiceRequest') -> bool:
        if self.available:
            print(f"\n{self.name} is confirming the request...")
            self.available = False
            self.current_request = request
            request.assign_provider(self)
            return True
        return False

    def reject_request(self, request: 'ServiceRequest') -> bool:
        print(f"\n{self.name} is rejecting the request")
        request.reject()
        return True

    def mark_service_completed(self) -> bool:
        if self.current_request:
            print(f"\n{self.name} marks service as completed")
            self.current_request.complete()
            self.available = True
            self.current_request = None
            return True
        return False


class ServiceRequest:
    def __init__(self, request_id: int, user: User, problem_details: str, location: Tuple[float, float]):
        self.request_id = request_id
        self.user = user
        self.problem_details = problem_details
        self.location = location
        self.provider: Optional[Provider] = None
        self.status = "pending"  # pending, assigned, completed, rejected
        self.review: Optional[Dict[str, any]] = None

    def assign_provider(self, provider: Provider) -> None:
        self.provider = provider
        self.status = "assigned"
        print(f"Provider {provider.name} assigned to request {self.request_id}")

    def reject(self) -> None:
        self.status = "rejected"
        print(f"Request {self.request_id} rejected")

    def complete(self) -> None:
        self.status = "completed"
        print(f"Request {self.request_id} completed")

    def add_review(self, rating: int, comment: str) -> None:
        self.review = {"rating": rating, "comment": comment}
        print(f"Review added to request {self.request_id}")


class ServiceSystem:
    def __init__(self):
        self.providers: List[Provider] = []
        self.requests: List[ServiceRequest] = []
        self.request_counter = 1

    def add_provider(self, provider: Provider) -> None:
        self.providers.append(provider)

    def find_nearest_available_provider(self, location: Tuple[float, float]) -> Optional[Provider]:
        available_providers = [p for p in self.providers if p.available]
        if not available_providers:
            return None
        
        
        return random.choice(available_providers)

    def process_request(self, user: User, problem_details: str, location: Tuple[float, float]) -> Optional[ServiceRequest]:
        request = ServiceRequest(self.request_counter, user, problem_details, location)
        self.request_counter += 1
        self.requests.append(request)

        provider = self.find_nearest_available_provider(location)
        if provider:
            # Simulate provider decision (80% chance to accept)
            if random.random() < 0.8:
                provider.confirm_request(request)
            else:
                provider.reject_request(request)
        else:
            print("No available providers at this time")

        return request


def main():
    system = ServiceSystem()

    system.add_provider(Provider(1, "Provider Alpha", (40.7128, -74.0060)))  # NYC
    system.add_provider(Provider(2, "Provider Beta", (40.7129, -74.0061)))
    system.add_provider(Provider(3, "Provider Gamma", (40.7127, -74.0059)))

    # Create a user
    user = User(1, "John Smith", (40.7128, -74.0060))

    print("\n=== Starting Service Request Flow ===")
    
    #User submits request
    request = user.submit_request("Plumbing issue in kitchen", system)
    
    if request and request.status == "assigned":
        #User views provider details
        user.view_provider_details()
        
        #User tracks provider location
        user.track_provider()
        
        #Provider completes service
        request.provider.mark_service_completed()
        
        #User confirms completion (processes payment)
        user.confirm_completion()
        
        #User submits review
        user.submit_review(5, "Excellent service, arrived quickly and fixed the problem")
    
    print("\n=== Service Request Flow Completed ===")


if __name__ == "__main__":
    main()