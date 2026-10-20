import base64
import hashlib
import hmac

from spo_assistants.assistants.models import ChatMessage

class ChatIntegrityService:
    def __init__(self, secret: str) -> None:
        self._secret = secret.encode()

    def sign(self, user_id: str, history: list[ChatMessage]) -> str:
        payload = f"{user_id}\n" + "\n".join(f"{m.role}:{m.content}" for m in history)
        digest = hmac.new(self._secret, payload.encode(), hashlib.sha256).digest()
        return base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
    
    def verify(self, user_id: str, history: list[ChatMessage], signature: str) -> bool:
        return hmac.compare_digest(self.sign(user_id, history), signature)