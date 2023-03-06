import dataclasses as dc
import typing as t


@dc.dataclass(frozen=True, slots=True)
class Group:
    id: int
    name: str

    @classmethod
    def of(cls, d: dict[str, t.Any]) -> t.Self:
        return cls(id=d.get("id"), name=d.get("name"))

    def full_name(self) -> str:
        return self.name
