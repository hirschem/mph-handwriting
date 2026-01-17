from pathlib import Path
from fastapi import UploadFile
from typing import Optional
import json
import aiofiles
from app.models.schemas import ProposalData

BASE_DIR = Path(__file__).parent.parent.parent.parent


class FileManager:
    def __init__(self):
        self.data_dir = BASE_DIR / "data"
        self.uploads_dir = self.data_dir / "raw_uploads"
        self.sessions_dir = self.data_dir / "sessions"
        self.ground_truth_dir = self.data_dir / "ground_truth"
        
        # Create directories
        self.uploads_dir.mkdir(parents=True, exist_ok=True)
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self.ground_truth_dir.mkdir(parents=True, exist_ok=True)
    
    async def save_upload(self, session_id: str, file: UploadFile) -> Path:
        """Save uploaded image to raw_uploads and session directory"""
        
        session_dir = self.sessions_dir / session_id
        session_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = session_dir / f"original_{file.filename}"
        
        async with aiofiles.open(file_path, "wb") as f:
            content = await file.read()
            await f.write(content)
        
        return file_path
    
    async def save_transcription(self, session_id: str, text: str):
        """Save raw transcription to session directory"""
        
        session_dir = self.sessions_dir / session_id
        session_dir.mkdir(parents=True, exist_ok=True)
        
        async with aiofiles.open(session_dir / "transcription.txt", "w") as f:
            await f.write(text)
    
    async def save_proposal(self, session_id: str, proposal_data: ProposalData):
        """Save structured proposal data to session directory"""
        
        session_dir = self.sessions_dir / session_id
        session_dir.mkdir(parents=True, exist_ok=True)
        
        async with aiofiles.open(session_dir / "proposal.json", "w") as f:
            await f.write(proposal_data.model_dump_json(indent=2))
    
    async def load_proposal(self, session_id: str) -> Optional[ProposalData]:
        """Load proposal data from session directory"""
        
        proposal_path = self.sessions_dir / session_id / "proposal.json"
        
        if not proposal_path.exists():
            return None
        
        async with aiofiles.open(proposal_path, "r") as f:
            content = await f.read()
            data = json.loads(content)
            return ProposalData(**data)
