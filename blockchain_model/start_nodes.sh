#!/bin/bash

echo "Starting Blockchain Node 1 on port 5000..."
PORT=5000 python3 -m uvicorn node:app --port 5000 --host 0.0.0.0 &
PID1=$!

echo "Starting Blockchain Node 2 on port 5001..."
PORT=5001 python3 -m uvicorn node:app --port 5001 --host 0.0.0.0 &
PID2=$!

echo "Starting Blockchain Node 3 on port 5002..."
PORT=5002 python3 -m uvicorn node:app --port 5002 --host 0.0.0.0 &
PID3=$!

echo "Waiting for nodes to start..."
sleep 3

echo "Registering nodes with each other..."

# Register Node 2 and 3 with Node 1
curl -X POST http://127.0.0.1:5000/nodes/register \
     -H "Content-Type: application/json" \
     -d '{"nodes": ["http://127.0.0.1:5001", "http://127.0.0.1:5002"]}'

# Register Node 1 and 3 with Node 2
curl -X POST http://127.0.0.1:5001/nodes/register \
     -H "Content-Type: application/json" \
     -d '{"nodes": ["http://127.0.0.1:5000", "http://127.0.0.1:5002"]}'

# Register Node 1 and 2 with Node 3
curl -X POST http://127.0.0.1:5002/nodes/register \
     -H "Content-Type: application/json" \
     -d '{"nodes": ["http://127.0.0.1:5000", "http://127.0.0.1:5001"]}'

echo "All 3 nodes are running and connected!"
echo "Press Ctrl+C to stop all nodes."

# Wait for Ctrl+C
trap 'kill $PID1 $PID2 $PID3; exit' SIGINT
wait
