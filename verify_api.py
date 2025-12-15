import requests
import sys

BASE_URL = 'http://127.0.0.1:8000/api'

def test_registration():
    print("Testing Registration...")
    url = f"{BASE_URL}/auth/register/"
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
    }
    response = requests.post(url, json=data)
    if response.status_code == 201:
        print("Registration Successful")
        return True
    elif response.status_code == 400 and "username" in response.json() and "already exists" in str(response.json()):
        print("User already exists (Expected if re-running)")
        return True
    else:
        print(f"Registration Failed: {response.status_code} {response.text}")
        return False

def test_login():
    print("Testing Login...")
    url = f"{BASE_URL}/auth/login/"
    data = {"username": "testuser", "password": "testpassword123"}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Login Successful")
        return response.json()['access']
    else:
        print(f"Login Failed: {response.status_code} {response.text}")
        return None

def test_create_category(token):
    print("Testing Create Category...")
    url = f"{BASE_URL}/recipes/categories/"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"name": "Test Category"}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        print("Category Created")
        return response.json()['id']
    else:
        print(f"Create Category Failed: {response.status_code} {response.text}")
        return None

def test_create_recipe(token, category_id):
    print("Testing Create Recipe...")
    url = f"{BASE_URL}/recipes/"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "title": "Test Recipe",
        "description": "A delicious test recipe",
        "ingredients": "Flour, Sugar, Eggs",
        "instructions": "Mix and bake",
        "category": category_id
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        print("Recipe Created")
        return response.json()['id']
    else:
        print(f"Create Recipe Failed: {response.status_code} {response.text}")
        return None

def main():
    if not test_registration():
        sys.exit(1)
    
    token = test_login()
    if not token:
        sys.exit(1)
    
    cat_id = test_create_category(token)
    if not cat_id:
        # Try to fetch existing category if creation failed due to unique constraint (though name isn't unique in model)
        # But for now assume failure
        pass # proceed to check if we can list/use existing?
    
    # If category creation failed, we might need a category id. 
    # For this simple test, we assume success or user needs to fix db.
    if cat_id:
        recipe_id = test_create_recipe(token, cat_id)

if __name__ == "__main__":
    main()
