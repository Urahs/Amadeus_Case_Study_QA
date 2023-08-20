import requests

api_url = "https://flights-api.buraky.workers.dev/"

def test_get_request_returns_200_status():
    response = requests.get(api_url)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    print("Get request returns 200 status: passed!")


def test_response_content():
    response = requests.get(api_url)
    
    response_data = response.json()
    assert "data" in response_data, "Response doesn't contain 'data' field"
    
    flights = response_data["data"]
    assert isinstance(flights, list), "The 'data' field should be a list"
    
    for flight in flights:
        assert isinstance(flight, dict), "Each item in 'data' should be a dictionary"
        assert "id" in flight and "from" in flight and "to" in flight and "date" in flight, "Flight structure is incorrect"
    
    print("Response content is correct: passed!")


def test_response_header():
    response = requests.get(api_url)
    
    content_type_header = response.headers.get("Content-Type")
    assert content_type_header is not None, "Response doesn't contain 'Content-Type' header"
    
    assert content_type_header == "application/json", f"Expected 'Content-Type' header to be 'application/json', but got '{content_type_header}'"

    print("Header control: passed!")

if __name__ == "__main__":
    test_get_request_returns_200_status()
    test_response_content()
    test_response_header()