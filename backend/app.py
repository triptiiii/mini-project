from fastapi import FastAPI, File, UploadFile
from .utils import file_sha256
from . import blockchain

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    sha256_hash = file_sha256(contents)

    # Add to blockchain
    new_block = blockchain.create_new_block(blockchain.blockchain[-1], sha256_hash)
    blockchain.blockchain.append(new_block)

    return {
        "filename": file.filename,
        "sha256": sha256_hash,
        "block_index": new_block.index,
        "block_hash": new_block.hash
    }

@app.get("/chain")
def get_chain():
    chain_data = [
        {
            "index": block.index,
            "timestamp": block.timestamp,
            "data": block.data,
            "hash": block.hash,
            "previous_hash": block.previous_hash
        }
        for block in blockchain.blockchain
    ]
    return {"length": len(chain_data), "chain": chain_data}
