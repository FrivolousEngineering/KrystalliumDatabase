import enum

from sqlmodel import SQLModel, Field, Relationship
from fastapi_jsonapi.schema_base import Field as JsonApiField
from fastapi_jsonapi.schema_base import RelationshipInfo as JsonApiRelationship


class Action(enum.StrEnum):
    Increasing = "increasing"
    Decreasing = "decreasing"
    Creating = "creating"
    Destroying = "destroying"
    Expanding = "expanding"
    Contracting = "contracting"
    Fortifying = "fortifying"
    Deteriorating = "deteriorating"
    Lightening = "lightening"
    Encumbering = "encumbering"
    Heating = "heating"
    Cooling = "cooling"
    Conducting = "conducting"
    Insulating = "insulating"
    Absorbing = "absorbing"
    Releasing = "releasing"
    Solidifying = "solidifying"


class Target(enum.StrEnum):
    Solid = "solid"
    Liquid = "liquid"
    Gas = "gas"
    Krystal = "krystal"
    Flesh = "flesh"
    Plant = "plant"
    Energy = "energy"
    Light = "light"
    Sound = "sound"
    Mind = "mind"


class Effect(SQLModel, table = True):
    id: int = Field(primary_key = True)
    name: str
    action: Action
    target: Target
    strength: int

    # Workaround to disable iteration so FastAPI-JSONAPI can handle
    # these properly.
    __iter__ = None
    __next__ = None


class SampleBase(SQLModel):
    id: int = Field(primary_key = True)
    rfid_id: str | None = None
    strength: int = 0


class RawSample(SampleBase, table = True):
    positive_action: Action
    positive_target: Target
    negative_action: Action
    negative_target: Target
    depleted: bool = False


class RefinedSample(SampleBase, table = True):
    primary_action: Action
    primary_target: Target
    secondary_action: Action
    secondary_target: Target


class BloodSampleEffectRelationship(SQLModel, table = True):
    sample_id: int = Field(foreign_key = "bloodsample.id", primary_key = True)
    effect_id: int = Field(foreign_key = "effect.id", primary_key = True)


class BloodSampleBase(SampleBase):
    pass


class BloodSample(BloodSampleBase, table = True):
    effect: Effect | None = Relationship(link_model = BloodSampleEffectRelationship)

    __iter__ = None
    __next__ = None


class BloodSampleJsonApi(BloodSampleBase):
    effect: Effect | None = JsonApiField(default = None, relationship = JsonApiRelationship(resource_type = "effect"))


class EnlistedEffectRelationship(SQLModel, table = True):
    enlisted_id: int = Field(foreign_key = "enlisted.id", primary_key = True)
    effect_id: int = Field(foreign_key = "effect.id", primary_key = True)


class EnlistedBase(SQLModel):
    id: int = Field(primary_key = True)

    name: str
    number: str


class Enlisted(EnlistedBase, table = True):
    effects: list[Effect] = Relationship(link_model = EnlistedEffectRelationship)

    __iter__ = None
    __next__ = None


class EnlistedJsonApi(EnlistedBase):
    effects: list[Effect] | None = JsonApiField(default = None, relationship = JsonApiRelationship(resource_type = "effect", many = True))
