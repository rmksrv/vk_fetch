import dataclasses as dc
import typing as t


@dc.dataclass(frozen=True, slots=True)
class User:
    id: int
    first_name: str
    last_name: str
    is_closed: bool
    can_access_closed: bool
    deactivated: str | None = None

    @classmethod
    def of(cls, d: dict[str, t.Any]) -> t.Self:
        return cls(
            id=d.get("id"),
            first_name=d.get("first_name"),
            last_name=d.get("last_name"),
            is_closed=d.get("is_closed"),
            can_access_closed=d.get("can_access_closed"),
            deactivated=d.get("deactivated"),
        )

    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
