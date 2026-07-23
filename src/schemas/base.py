from pydantic import BaseModel, ConfigDict


def _camelize(s: str) -> str:
    if "_" in s:
        parts = s.split("_")
        return parts[0] + "".join(p.capitalize() for p in parts[1:])
    return s[0].lower() + s[1:] if s else s


class APIBase(BaseModel):
    model_config = ConfigDict(
        alias_generator=_camelize,
        populate_by_name=True,
        from_attributes=True,
    )
