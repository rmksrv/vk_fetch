import enum


class MediaType(enum.Enum):
    Photo = "photo"
    Video = "video"
    Audio = "audio"
    Doc = "doc"
    Link = "link"
    Market = "market"
    Wall = "wall"


class Sex(enum.Enum):
    Female = 1
    Male = 2
    Undefined = 0


class Relation(enum.Enum):
    # не женат/не замужем
    NotMarried = 1
    # есть друг/есть подруга
    HasFriend = 2
    # помолвлен/помолвлена
    Engaged = 3
    # женат/замужем
    Married = 4
    # всё сложно
    Complicated = 5
    # в активном поиске
    InActiveSearch = 6
    # влюблён/влюблена
    InLove = 7
    # в гражданском браке
    CivilMarriage = 8
    # не указано
    Undefined = 0
