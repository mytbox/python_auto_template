import requests
import json

BASE_URL = "http://127.0.0.1:48080"

def test_health():
    print("\n=== Testing Health Check ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_send_verify_code():
    print("\n=== Testing Send Verification Code ===")
    data = {
        "loginType": "email",
        "number": "test@example.com"
    }
    response = requests.post(f"{BASE_URL}/account/send-verify-code", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    if response.status_code == 200:
        return response.json()['data']['code']
    return None

def test_login_with_code(code):
    print("\n=== Testing Login with Verification Code ===")
    data = {
        "loginType": "email",
        "number": "test@example.com",
        "authCode": code,
        "deviceType": "web",
        "language": "zh"
    }
    response = requests.post(f"{BASE_URL}/account/reg-ai-login", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_get_posts():
    print("\n=== Testing Get Posts ===")
    response = requests.get(f"{BASE_URL}/api/posts")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_get_post():
    print("\n=== Testing Get Post by ID ===")
    response = requests.get(f"{BASE_URL}/api/posts/1")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_create_post():
    print("\n=== Testing Create Post ===")
    data = {
        "title": "Test Post",
        "body": "This is a test post",
        "userId": 1
    }
    response = requests.post(f"{BASE_URL}/api/posts", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_update_post():
    print("\n=== Testing Update Post ===")
    data = {
        "title": "Updated Post",
        "body": "This is an updated post",
        "userId": 1
    }
    response = requests.put(f"{BASE_URL}/api/posts/1", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_delete_post():
    print("\n=== Testing Delete Post ===")
    response = requests.delete(f"{BASE_URL}/api/posts/1")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_get_users():
    print("\n=== Testing Get Users ===")
    response = requests.get(f"{BASE_URL}/api/users")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_create_user():
    print("\n=== Testing Create User ===")
    data = {
        "name": "Test User",
        "email": "test@example.com",
        "phone": "13800138000"
    }
    response = requests.post(f"{BASE_URL}/api/users", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_get_comments():
    print("\n=== Testing Get Comments ===")
    response = requests.get(f"{BASE_URL}/api/comments")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    print("=" * 50)
    print("Mock API Server Test Suite")
    print("=" * 50)
    
    try:
        test_health()
        test_get_posts()
        test_get_post()
        test_create_post()
        test_update_post()
        test_delete_post()
        test_get_users()
        test_create_user()
        test_get_comments()
        
        code = test_send_verify_code()
        if code:
            test_login_with_code(code)
        
        print("\n" + "=" * 50)
        print("All tests completed!")
        print("=" * 50)
        
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to Mock API Server")
        print("Please make sure the server is running on http://127.0.0.1:48080")
    except Exception as e:
        print(f"\nError: {e}")
