import enum

import vk_api as vk


VK_MAX_ITEMS_COUNT = 200
VK_GROUP_PEER_ID_SINCE = 2000000000
KATE_MOBILE_APP_ID = 2685278

DEFAULT_USER_PERMISSIONS_SCOPE = frozenset(
    [
        vk.VkUserPermissions.MESSAGES,
        vk.VkUserPermissions.PHOTOS,
        vk.VkUserPermissions.STATUS,
        vk.VkUserPermissions.VIDEO,
    ]
)


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


class ConversationType(enum.Enum):
    User = "user"
    Chat = "chat"
    Group = "group"
    Email = "email"


class ConversationState(enum.Enum):
    In = "in"
    Kicked = "kicked"
    Left = "left"
