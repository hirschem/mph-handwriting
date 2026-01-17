"""
Evaluate transcription accuracy against ground truth
"""
from pathlib import Path
import difflib


def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate similarity ratio between two texts"""
    return difflib.SequenceMatcher(None, text1, text2).ratio()


def eval_accuracy():
    """Evaluate transcription accuracy"""
    
    ground_truth_dir = Path("data/ground_truth")
    
    if not ground_truth_dir.exists():
        print(f"Ground truth directory not found: {ground_truth_dir}")
        return
    
    results = []
    
    for session_dir in ground_truth_dir.iterdir():
        if not session_dir.is_dir():
            continue
        
        transcription_file = session_dir / "transcription.txt"
        corrected_file = session_dir / "corrected.txt"
        
        if transcription_file.exists() and corrected_file.exists():
            with open(transcription_file) as f:
                transcription = f.read()
            
            with open(corrected_file) as f:
                ground_truth = f.read()
            
            similarity = calculate_similarity(transcription, ground_truth)
            
            results.append({
                "session_id": session_dir.name,
                "similarity": similarity
            })
            
            print(f"{session_dir.name}: {similarity:.2%}")
    
    if results:
        avg_similarity = sum(r["similarity"] for r in results) / len(results)
        print(f"\nAverage accuracy: {avg_similarity:.2%}")
    else:
        print("No ground truth data found")


if __name__ == "__main__":
    eval_accuracy()
