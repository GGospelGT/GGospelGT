#!/usr/bin/env python3
"""
Debug script to test messaging system and identify the 500 error
"""

import requests
import json
import uuid

BACKEND_URL = "http://localhost:8001/api"

def test_message_debug():
    """Debug the messaging system error"""
    
    # First, create and authenticate users
    homeowner_data = {
        "name": "Test Homeowner",
        "email": f"test.homeowner.{uuid.uuid4().hex[:8]}@email.com",
        "password": "SecurePass123",
        "phone": "08123456789",
        "location": "Lagos, Lagos State",
        "postcode": "100001"
    }
    
    tradesperson_data = {
        "name": "Test Tradesperson",
        "email": f"test.tradesperson.{uuid.uuid4().hex[:8]}@tradework.com",
        "password": "SecurePass123",
        "phone": "08187654321",
        "location": "Abuja, FCT",
        "postcode": "900001",
        "trade_categories": ["Plumbing"],
        "experience_years": 5,
        "company_name": "Test Plumbing",
        "description": "Professional plumber with 5 years experience.",
        "certifications": ["Licensed Plumber"]
    }
    
    # Register homeowner
    response = requests.post(f"{BACKEND_URL}/auth/register/homeowner", json=homeowner_data)
    print(f"Homeowner registration: {response.status_code}")
    if response.status_code != 200:
        print(f"Error: {response.text}")
        return
    
    # Register tradesperson
    response = requests.post(f"{BACKEND_URL}/auth/register/tradesperson", json=tradesperson_data)
    print(f"Tradesperson registration: {response.status_code}")
    if response.status_code != 200:
        print(f"Error: {response.text}")
        return
    
    # Login homeowner
    response = requests.post(f"{BACKEND_URL}/auth/login", 
                           json={"email": homeowner_data["email"], "password": homeowner_data["password"]})
    print(f"Homeowner login: {response.status_code}")
    if response.status_code != 200:
        print(f"Error: {response.text}")
        return
    homeowner_token = response.json()['access_token']
    homeowner_id = response.json()['user']['id']
    
    # Login tradesperson
    response = requests.post(f"{BACKEND_URL}/auth/login", 
                           json={"email": tradesperson_data["email"], "password": tradesperson_data["password"]})
    print(f"Tradesperson login: {response.status_code}")
    if response.status_code != 200:
        print(f"Error: {response.text}")
        return
    tradesperson_token = response.json()['access_token']
    tradesperson_id = response.json()['user']['id']
    
    # Create a job
    job_data = {
        "title": "Test Plumbing Job for Messaging",
        "description": "This is a test job to test the messaging system functionality.",
        "category": "Plumbing",
        "location": "Lagos, Lagos State",
        "postcode": "100001",
        "budget_min": 50000,
        "budget_max": 100000,
        "timeline": "Within 1 week",
        "homeowner_name": homeowner_data['name'],
        "homeowner_email": homeowner_data['email'],
        "homeowner_phone": homeowner_data['phone']
    }
    
    response = requests.post(f"{BACKEND_URL}/jobs/", 
                           json=job_data,
                           headers={'Authorization': f'Bearer {homeowner_token}'})
    print(f"Job creation: {response.status_code}")
    if response.status_code != 200:
        print(f"Error: {response.text}")
        return
    job_id = response.json()['id']
    
    # Create a quote (needed for messaging authorization)
    quote_data = {
        "job_id": job_id,
        "price": 75000,
        "message": "I can complete this job within your timeline and budget.",
        "estimated_duration": "3-5 days",
        "start_date": "2024-01-15T10:00:00"
    }
    
    response = requests.post(f"{BACKEND_URL}/quotes/", 
                           json=quote_data,
                           headers={'Authorization': f'Bearer {tradesperson_token}'})
    print(f"Quote creation: {response.status_code}")
    if response.status_code != 200:
        print(f"Error: {response.text}")
        return
    
    # Now test messaging - homeowner sends first message
    message_data = {
        'job_id': job_id,
        'recipient_id': tradesperson_id,
        'content': 'Hello, I have some questions about your quote.',
        'message_type': 'text'
    }
    
    response = requests.post(f"{BACKEND_URL}/messages/send", 
                           data=message_data,
                           headers={'Authorization': f'Bearer {homeowner_token}'})
    print(f"Homeowner message: {response.status_code}")
    if response.status_code != 200:
        print(f"Error: {response.text}")
        return
    
    # Test tradesperson reply - this is where the error occurs
    reply_data = {
        'job_id': job_id,
        'recipient_id': homeowner_id,
        'content': 'Thank you for your message. I would be happy to answer your questions.',
        'message_type': 'text'
    }
    
    print(f"\nTesting tradesperson reply...")
    print(f"Job ID: {job_id}")
    print(f"Homeowner ID: {homeowner_id}")
    print(f"Tradesperson ID: {tradesperson_id}")
    
    response = requests.post(f"{BACKEND_URL}/messages/send", 
                           data=reply_data,
                           headers={'Authorization': f'Bearer {tradesperson_token}'})
    print(f"Tradesperson reply: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code != 200:
        # Try to get more details
        try:
            error_data = response.json()
            print(f"Error details: {json.dumps(error_data, indent=2)}")
        except:
            print("Could not parse error response as JSON")

if __name__ == "__main__":
    test_message_debug()