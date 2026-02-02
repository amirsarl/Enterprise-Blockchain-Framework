"""
Core Block implementation for Enterprise Blockchain Framework
"""
"""
by sarl
"""

import hashlib
import json
import time
from dataclasses import dataclass, asdict
from typing import List, Dict, Any
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

@dataclass
class Transaction:
    """Enterprise-grade transaction structure"""
    sender: str
    recipient: str
    amount: float
    timestamp: float
    signature: str = None
    metadata: Dict[str, Any] = None
    
    def to_dict(self) -> Dict:
        """Convert transaction to dictionary"""
        return asdict(self)
    
    def hash(self) -> str:
        """Calculate transaction hash"""
        tx_string = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(tx_string.encode()).hexdigest()

class Block:
    """Production-ready Block implementation"""
    
    def __init__(
        self,
        index: int,
        timestamp: float,
        transactions: List[Transaction],
        previous_hash: str,
        validator: str = None,
        nonce: int = 0
    ):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.validator = validator
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calculate block hash using SHA-256"""
        block_data = {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [tx.hash() for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'validator': self.validator,
            'nonce': self.nonce
        }
        block_string = json.dumps(block_data, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int) -> None:
        """Proof of Work mining implementation"""
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
    
    def to_dict(self) -> Dict:
        """Serialize block to dictionary"""
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'hash': self.hash,
            'validator': self.validator,
            'nonce': self.nonce
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Block':
        """Deserialize block from dictionary"""
        transactions = [
            Transaction(**tx) for tx in data['transactions']
        ]
        block = cls(
            index=data['index'],
            timestamp=data['timestamp'],
            transactions=transactions,
            previous_hash=data['previous_hash'],
            validator=data.get('validator'),
            nonce=data.get('nonce', 0)
        )
        block.hash = data['hash']
        return block

class Blockchain:
    """Enterprise Blockchain Implementation"""
    
    def __init__(self, difficulty: int = 4):
        self.chain: List[Block] = []
        self.pending_transactions: List[Transaction] = []
        self.difficulty = difficulty
        self.create_genesis_block()
    
    def create_genesis_block(self) -> None:
        """Create the first block in the chain"""
        genesis_block = Block(
            index=0,
            timestamp=time.time(),
            transactions=[],
            previous_hash="0" * 64,
            validator="genesis"
        )
        genesis_block.hash = genesis_block.calculate_hash()
        self.chain.append(genesis_block)
    
    def get_latest_block(self) -> Block:
        """Get the most recent block"""
        return self.chain[-1]
    
    def add_transaction(self, transaction: Transaction) -> None:
        """Add a new transaction to pending transactions"""
        self.pending_transactions.append(transaction)
    
    def mine_pending_transactions(self, validator_address: str) -> Block:
        """Mine all pending transactions"""
        block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            transactions=self.pending_transactions,
            previous_hash=self.get_latest_block().hash,
            validator=validator_address
        )
        block.mine_block(self.difficulty)
        self.chain.append(block)
        self.pending_transactions = []
        return block
    
    def is_chain_valid(self) -> bool:
        """Validate the entire blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check current block hash
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Check chain linkage
            if current_block.previous_hash != previous_block.hash:
                return False
            
            # Check Proof of Work
            if current_block.hash[:self.difficulty] != '0' * self.difficulty:
                return False
        
        return True
    
    def get_balance(self, address: str) -> float:
        """Calculate balance for an address"""
        balance = 0.0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender == address:
                    balance -= transaction.amount
                if transaction.recipient == address:
                    balance += transaction.amount
        return balance
