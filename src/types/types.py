from pydantic import BaseModel

#Message reçu
class Claims(BaseModel):
    claims: dict[int, str]


class ErroDetail(BaseModel):
    message: str
    type: str
    param: str
    code: str

class Error(BaseModel): 
    error:ErroDetail

class Message(BaseModel):
    role: str
    content: str

class Choice(BaseModel):
    index: int
    message: Message
    finish_reason: str

class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class Success(BaseModel):
	id: str
	object: str
	created: int
	model: str
	choices: list[Choice]
	usage: Usage


