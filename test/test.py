import os
import requests
import pymongo
import pprint
from urllib.parse import urlparse
from dotenv import load_dotenv

# --- Configuration ---
load_dotenv()

# Get API keys and DB URI from environment variables
API_KEY_V1 = os.getenv("API_KEY_V1")
API_KEY_V2 = os.getenv("API_KEY_V2") # This will be None for the candidate
MONGO_URI = os.getenv("MONGO_URI")
INVALID_KEY = "this-is-a-wrong-key"

BASE_URL = "http://localhost:8000/api"


# --- Helper Functions (No changes needed here) ---
def print_test_header(title):
    """Prints a formatted header for a test section."""
    print("\n" + "=" * 50)
    print(f"  {title}")
    print("=" * 50)


def print_result(test_name, success, reason=""):
    """Prints the result of a test in a standard format."""
    status = "SUCCESS" if success else "FAILURE"
    details = f" -> {reason}" if reason else ""
    print(f"[*] {test_name:<40} [{status}]{details}")


def verify_and_print_db_entries(collection, version, limit=2):
    """
    Queries the database for tickets of a specific version and prints them
    to verify they were created correctly.
    """
    print(f"\n--- Verifying Database for version '{version}' ---")
    try:
        documents = list(collection.find({"endpoint_version": version}).limit(limit))
        if not documents:
            print("[INFO] No documents found in DB for this version.")
            return
        print(f"[INFO] Found {len(documents)} sample document(s) for version '{version}':")
        for doc in documents:
            pprint.pprint(doc)
            print("-" * 20)
        print("--- Database Verification Complete ---")
    except Exception as e:
        print(f"[ERROR] Failed to query database: {e}")


# --- Main Test Execution ---
def run_tests():
    """Executes all API test cases and database checks."""

    if not all([API_KEY_V1, MONGO_URI]):
        print("ERROR: API_KEY_V1 or MONGO_URI not found in .env file. Please ensure the file is correct.")
        return

    # --- Database Connection Setup ---
    db_client = None
    try:
        print("Connecting to MongoDB...")
        db_client = pymongo.MongoClient(MONGO_URI)
        db_client.admin.command('ping')
        db_name = urlparse(MONGO_URI).path.lstrip('/')
        db = db_client[db_name]
        ticket_collection = db["tickets"]
        print(f"Successfully connected to MongoDB database '{db_name}'.")
    except Exception as e:
        print(f"\n[FAILURE] Could not connect to MongoDB. Is the Docker container running? Error: {e}")
        return

    print_test_header("Running API Endpoint Tests")

    try:
        # --- Test Case 1: V1 Endpoint with Valid Key ---
        headers_v1 = {"X-API-KEY": API_KEY_V1}
        response_v1 = requests.get(f"{BASE_URL}/v1/tickets", headers=headers_v1, timeout=10)
        is_success_v1 = response_v1.status_code == 200 and isinstance(response_v1.json(), list) and len(response_v1.json()) > 0
        print_result("V1 Endpoint - Valid Key", is_success_v1, f"Status: {response_v1.status_code}")
        if is_success_v1:
            verify_and_print_db_entries(ticket_collection, "v1")

        # --- Test Case 3 (reordered): V1 Endpoint with Invalid Key ---
        headers_invalid = {"X-API-KEY": INVALID_KEY}
        response_v1_fail = requests.get(f"{BASE_URL}/v1/tickets", headers=headers_invalid, timeout=10)
        is_success = response_v1_fail.status_code == 401
        print_result("V1 Endpoint - Invalid Key", is_success, f"Status: {response_v1_fail.status_code} (Expected 401)")

        # --- MODIFIED: Make V2 tests conditional ---
        # Only run these tests if the API_KEY_V2 is actually set in the environment.
        if API_KEY_V2:
            print("\n--- Running V2 Endpoint Tests (API_KEY_V2 found) ---")

            # Test Case 2: V2 Endpoint with Valid Key
            headers_v2 = {"X-API-KEY": API_KEY_V2}
            response_v2 = requests.get(f"{BASE_URL}/v2/tickets", headers=headers_v2, timeout=10)
            is_success_v2 = response_v2.status_code == 200 and isinstance(response_v2.json(), list) and len(response_v2.json()) > 0
            print_result("V2 Endpoint - Valid Key", is_success_v2, f"Status: {response_v2.status_code}")
            if is_success_v2:
                verify_and_print_db_entries(ticket_collection, "v2")

            # Test Case 4: V2 Endpoint with Invalid Key
            response_v2_fail = requests.get(f"{BASE_URL}/v2/tickets", headers=headers_invalid, timeout=10)
            is_success = response_v2_fail.status_code == 401
            print_result("V2 Endpoint - Invalid Key", is_success, f"Status: {response_v2_fail.status_code} (Expected 401)")
        else:
            print("\n[INFO] API_KEY_V2 not found in .env file. Skipping V2 endpoint tests.")


    except requests.exceptions.ConnectionError:
        print("\n[FAILURE] Connection failed. Is the API service running in Docker?")
        print("          Run 'docker compose up' in another terminal before starting the tests.")
    except Exception as e:
        print(f"\n[FAILURE] An unexpected error occurred: {e}")
    finally:
        if db_client:
            db_client.close()
            print("\nMongoDB connection closed.")


if __name__ == "__main__":
    run_tests()