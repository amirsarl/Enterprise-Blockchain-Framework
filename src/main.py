"""
Enterprise Blockchain Framework - Main Entry Point
Enterprise Blockchain Framework - نقطه شروع اصلی
"""

import asyncio
import logging
from typing import Optional
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Enterprise Blockchain Framework",
    description="A production-ready blockchain framework for enterprise applications",
    version="1.0.0",
    contact={
        "name": "Enterprise Blockchain Team",
        "url": "https://github.com/amirsarl/Enterprise-Blockchain-Framework",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0",
    },
)

class BlockchainStatus(BaseModel):
    """مدل وضعیت بلاکچین / Blockchain status model"""
    status: str
    version: str
    network: str
    block_height: Optional[int] = None
    peer_count: Optional[int] = None

@app.get("/", tags=["Root"])
async def read_root():
    """صفحه اصلی / Home page"""
    return {
        "message": "Welcome to Enterprise Blockchain Framework API",
        "documentation": "/docs",
        "repository": "https://github.com/amirsarl/Enterprise-Blockchain-Framework",
    }

@app.get("/status", response_model=BlockchainStatus, tags=["Blockchain"])
async def get_blockchain_status():
    """دریافت وضعیت بلاکچین / Get blockchain status"""
    return BlockchainStatus(
        status="active",
        version="1.0.0",
        network="testnet",
        block_height=0,
        peer_count=0,
    )

@app.get("/health", tags=["Health"])
async def health_check():
    """بررسی سلامت سرویس / Health check"""
    return {"status": "healthy", "timestamp": asyncio.get_event_loop().time()}

class Transaction(BaseModel):
    """مدل تراکنش / Transaction model"""
    sender: str
    receiver: str
    amount: float
    asset: str = "ETH"

@app.post("/transactions", tags=["Transactions"])
async def create_transaction(transaction: Transaction):
    """ایجاد تراکنش جدید / Create new transaction"""
    logger.info(f"New transaction: {transaction.sender} -> {transaction.receiver}")
    
    # Simulate transaction processing
    tx_hash = f"0x{hash(str(transaction.dict())):064x}"
    
    return {
        "message": "Transaction created successfully",
        "transaction_hash": tx_hash,
        "status": "pending",
    }

@app.get("/blocks/latest", tags=["Blocks"])
async def get_latest_block():
    """دریافت آخرین بلوک / Get latest block"""
    return {
        "block_number": 0,
        "timestamp": "2024-01-01T00:00:00Z",
        "transaction_count": 0,
        "miner": "genesis",
        "hash": "0x0000000000000000000000000000000000000000",
    }

if __name__ == "__main__":
    logger.info("Starting Enterprise Blockchain Framework API...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload in development
    )
