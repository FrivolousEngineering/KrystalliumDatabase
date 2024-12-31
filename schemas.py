import pydantic


class SampleBase(pydantic.BaseModel):
    id: str
    rfid_id: str|None = None
    strength: int

    class Config:
        orm_mode = True


class RawSample(SampleBase):
    positive_action: str
    positive_target: str
    negative_action: str
    negative_target: str
    depleted: bool = False


class RefinedSample(SampleBase):
    primary_action: str
    primary_target: str
    secondary_action: str
    secondary_target: str


class BloodSample(SampleBase):
    origin: str
    action: str
    target: str
