"""
Build JSONL training dataset from ground truth corrections
"""
from pathlib import Path
import json


def build_dataset():
    """Create JSONL dataset from ground truth folder"""
    
    ground_truth_dir = Path("data/ground_truth")
    output_file = Path("data/training_dataset.jsonl")
    
    if not ground_truth_dir.exists():
        print(f"Ground truth directory not found: {ground_truth_dir}")
        return
    
    dataset = []
    
    # Iterate through ground truth sessions
    for session_dir in ground_truth_dir.iterdir():
        if not session_dir.is_dir():
            continue
        
        transcription_file = session_dir / "transcription.txt"
        corrected_file = session_dir / "corrected.txt"
        
        if transcription_file.exists() and corrected_file.exists():
            with open(transcription_file) as f:
                raw_text = f.read()
            
            with open(corrected_file) as f:
                corrected_text = f.read()
            
            dataset.append({
                "session_id": session_dir.name,
                "raw_text": raw_text,
                "corrected_text": corrected_text
            })
    
    # Write JSONL
    with open(output_file, "w") as f:
        for item in dataset:
            f.write(json.dumps(item) + "\n")
    
    print(f"Created dataset with {len(dataset)} examples: {output_file}")


if __name__ == "__main__":
    build_dataset()
