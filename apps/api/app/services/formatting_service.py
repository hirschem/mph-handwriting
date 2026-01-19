from openai import AsyncOpenAI
from app.models.config import get_settings
from app.models.schemas import ProposalData
import json

settings = get_settings()


class FormattingService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
    
    async def rewrite_professional(self, raw_text: str) -> str:
        """Rewrite transcribed text in professional construction proposal language"""
        
        response = await self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional residential construction proposal writer. "
                        "Rewrite the provided text into a polished, professional proposal "
                        "suitable for sending to residential construction clients. "
                        "Maintain all scope, pricing, and timeline details. "
                        "Use clear, confident, professional language that inspires trust."
                    )
                },
                {
                    "role": "user",
                    "content": raw_text
                }
            ],
            max_tokens=2000
        )
        
        return response.choices[0].message.content
    
    async def structure_proposal(self, professional_text: str) -> ProposalData:
        """Extract structured data from professional proposal text"""
        
        response = await self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Extract structured data from this construction proposal. "
                        "Return a JSON object with: client_name, project_address, "
                        "scope_of_work (array), line_items (array with description, quantity, rate, amount), "
                        "subtotal, tax, total, payment_terms, timeline, notes. "
                        "IMPORTANT: For numeric fields (subtotal, tax, total, quantity, rate, amount), "
                        "use null if the value is not present or cannot be determined. "
                        "Do NOT use placeholder strings like '[Enter Amount]' - use null instead."
                    )
                },
                {
                    "role": "user",
                    "content": professional_text
                }
            ],
            response_format={"type": "json_object"}
        )
        
        data = json.loads(response.choices[0].message.content)
        
        # Clean up any string placeholders that slipped through
        for field in ['subtotal', 'tax', 'total']:
            if field in data and isinstance(data[field], str):
                data[field] = None
        
        if 'line_items' in data and data['line_items']:
            for item in data['line_items']:
                for field in ['quantity', 'rate', 'amount']:
                    if field in item and isinstance(item[field], str):
                        item[field] = None
        
        return ProposalData(**data)
