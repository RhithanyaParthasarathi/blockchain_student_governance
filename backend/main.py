from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from datetime import timedelta
import httpx
import os
from dotenv import load_dotenv

# Get the path to the .env file in the backend directory
base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, ".env")
load_dotenv(dotenv_path=env_path)

from backend.database import init_db, students_collection
from backend.models import StudentModel, StudentCreate, StudentResponse, Token, VoteSubmit
from backend.auth import (
    create_access_token, 
    get_password_hash, 
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    verify_password
)
from fastapi.responses import HTMLResponse
from backend.blockchain_client import blockchain_client

app = FastAPI(title="Student Governance Backend API")

@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard():
    dashboard_path = os.path.join(os.path.dirname(base_dir), "blockchain_model", "dashboard.html")
    with open(dashboard_path, "r") as f:
        return f.read()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    await init_db()

@app.post("/register", response_model=StudentResponse)
async def register_student(student: StudentCreate):
    existing_student = await students_collection.find_one({"roll_number": student.roll_number})
    if existing_student:
        raise HTTPException(status_code=400, detail="Roll number already registered")
        
    hashed_password = get_password_hash(student.password)
    student_dict = {
        "roll_number": student.roll_number,
        "password_hash": hashed_password,
        "is_eligible": True,
        "has_voted": False
    }
    
    await students_collection.insert_one(student_dict)
    return student_dict

@app.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    student = await students_collection.find_one({"roll_number": form_data.username})
    if not student or not verify_password(form_data.password, student["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": student["roll_number"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/elections")
async def get_elections():
    return {
        "status": "open",
        "candidates": [
            {"id": "cand_1", "name": "Abc", "position": "President"},
            {"id": "cand_2", "name": "Xyz", "position": "President"}
        ]
    }

@app.post("/vote")
async def submit_vote(vote: VoteSubmit, current_user: dict = Depends(get_current_user)):
    if current_user.get("has_voted"):
        raise HTTPException(status_code=400, detail="Student has already voted")
        
    if not current_user.get("is_eligible"):
        raise HTTPException(status_code=403, detail="Student is not eligible to vote")
        
    # Submit transaction to blockchain
    try:
        await blockchain_client.submit_vote(
            voter_id=current_user["roll_number"], 
            candidate_id=vote.candidate_id
        )
        
        # Trigger mining to confirm block
        #await blockchain_client.trigger_mine()
        
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Blockchain network error: {str(e)}")
        
    # Update DB state
    await students_collection.update_one(
        {"roll_number": current_user["roll_number"]},
        {"$set": {"has_voted": True}}
    )
    
    return {"message": "Vote successfully cast and recorded on the blockchain"}

@app.get("/results")
async def get_results():
    try:
        chain_data = await blockchain_client.get_chain()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Blockchain network error: {str(e)}")
        
    chain = chain_data.get("chain", [])
    
    results = {}
    for block in chain:
        for tx in block.get("transactions", []):
            candidate_id = tx.get("candidate_id")
            if candidate_id:
                results[candidate_id] = results.get(candidate_id, 0) + 1
                
    return {"votes": results, "total_blocks": len(chain)}
