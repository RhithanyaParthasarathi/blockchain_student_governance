# Development Plan: Blockchain Student Governance System (2 Developers)

This plan splits the work into two distinct roles to allow parallel development with minimal overlap and clear integration points.

## Developer 1: Blockchain & Smart Contracts Engineer
**Focus:** Private blockchain infrastructure, smart contract logic, and on-chain security.

### Core Responsibilities:
1. **Private Network Setup:**
   - Choose and configure the permissioned/private blockchain environment (e.g., Hyperledger Besu, GoQuorum, or a local Geth Proof-of-Authority network).
   - Set up the validator nodes and ensure block mining/validation works as expected.
2. **Smart Contract Development:**
   - **Voter Registry Contract:** Manage the whitelisted student addresses to ensure only eligible students can interact with the vote.
   - **Election Contract:** Handle the core voting logic, tallying, and strict enforcement against double-voting (e.g., mapping `hasVoted` states).
   - **State Contract:** Admin controls for opening and closing the election.
3. **Vote Encryption & Anonymity:**
   - Implement the mechanism to keep votes anonymous on-chain (e.g., using Commit-Reveal schemes, or verifying zero-knowledge proofs if utilizing advanced cryptography, or simply storing off-chain encrypted payloads on-chain).
4. **Documentation & Viva Prep (Blockchain Side):**
   - Document the *Network Architecture*, *Node Setup steps*, and outline the *Smart Contract Architecture Justification*.

---

## Developer 2: Backend API & Integration Engineer
**Focus:** Off-chain logic, REST APIs, database integration, and bridging the app to the blockchain.

### Core Responsibilities:
1. **Database Setup:**
   - Configure a traditional database (e.g., PostgreSQL or MongoDB) to store non-sensitive metadata (student credentials, election metadata, candidate profiles).
2. **Backend Authentication & REST APIs:**
   - Build a robust backend server (e.g., Node.js/Express, Python/FastAPI or Django).
   - Implement user authentication (JWTs) to verify student identities before they are permitted to vote.
   - Create REST APIs for frontend consumption (e.g., `GET /elections`, `POST /login`, `GET /results`).
3. **Web3 Interoperability:**
   - Integrate Web3 libraries (e.g., `ethers.js` or `web3.py`) into the backend.
   - Securely manage the relayer wallet or map student accounts to blockchain addresses so the backend can submit the vote transactions to the smart contracts that Developer 1 built.
4. **Documentation & Viva Prep (Backend Side):**
   - Document the *Backend Code*, *Database Schema*, *API endpoints*, and *App Deployment steps*.

---

## Parallel Workflow & Integration Points (Collaboration Plan)

### Phase 1: Architecture Agreement (Together)
- Agree on the data structures (e.g., what does a "Vote" payload look like?, API request/response formats).
- **Dev 1** starts writing the Smart Contracts on a local testing framework (like Hardhat/Truffle).
- **Dev 2** starts building the Database and Authentication APIs using mock blockchain responses to simulate contract calls.

### Phase 2: The "Handoff"
- **Dev 1** deploys the contracts to a testnet/local network and provides **Dev 2** with the **Contract Addresses** and the **ABI (Application Binary Interface)**.
- **Dev 2** updates the backend code, plugging in the ABI and Contract Addresses, replacing the mock responses with actual Web3 blockchain calls.

### Phase 3: Integration & Testing (Together)
- Test the entire end-to-end pipeline:
  1. Student logs in via the Backend API.
  2. Student submits a Vote via the API.
  3. Backend relays the transaction to the Blockchain network.
  4. Smart Contract verifies the student hasn't double-voted and is eligible.
  5. Blockchain records and tallies the vote anonymously.
- Fix issues and finalize the end-to-end documentation.
