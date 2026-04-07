import requests
import time
import concurrent.futures

NODE_URL = "http://127.0.0.1:5000"
BACKEND_URL = "http://127.0.0.1:8000"

def send_vote(voter_id):
    try:
        # We'll use the raw node endpoint for speed in this test
        response = requests.post(f"{NODE_URL}/transactions/new", json={
            "voter_id": f"TEST_USER_{voter_id}",
            "candidate_id": "cand_1"
        })
        return response.status_code == 200
    except:
        return False

def run_tps_test(count=100):
    print(f"🚀 Starting Throughput Test: Sending {count} votes...")
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(send_vote, range(count)))
    
    end_time = time.time()
    duration = end_time - start_time
    success_count = sum(1 for r in results if r)
    
    tps = success_count / duration
    
    print("\n--- PERFORMANCE RESULTS ---")
    print(f"Total Requests: {count}")
    print(f"Successful Requests: {success_count}")
    print(f"Total Time: {duration:.2f} seconds")
    print(f"Throughput (TPS): {tps:.2f} votes/sec")
    print("---------------------------\n")
    print("Now mine a block on the dashboard to see them solidified!")

if __name__ == "__main__":
    run_tps_test(50)
