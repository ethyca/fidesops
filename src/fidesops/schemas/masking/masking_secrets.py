from pydantic import BaseModel


class MaskingSecret(BaseModel):
    secret: str
    masking_strategy: str
    secret_type: str
