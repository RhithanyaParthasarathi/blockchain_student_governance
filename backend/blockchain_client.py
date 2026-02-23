import httpx
import os

BLOCKCHAIN_NODE_URL = os.environ.get("BLOCKCHAIN_NODE_URL", "http://127.0.0.1:5000")

class BlockchainClient:
    def __init__(self, base_url: str = BLOCKCHAIN_NODE_URL):
        self.base_url = base_url

    async def submit_vote(self, voter_id: str, candidate_id: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/transactions/new",
                json={"voter_id": voter_id, "candidate_id": candidate_id}
            )
            response.raise_for_status()
            return response.json()
            
    async def get_chain(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/chain")
            response.raise_for_status()
            return response.json()
            
    async def trigger_mine(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/mine")
            response.raise_for_status()
            return response.json()

blockchain_client = BlockchainClient()
