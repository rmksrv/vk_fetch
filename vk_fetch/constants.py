import enum
import pathlib

import vk_api as vk

PROJECT_ROOT = pathlib.Path(__file__).parent.parent
LOGS_PATH = PROJECT_ROOT / "logs"
DEFAULT_USER_PERMISSIONS_SCOPE = frozenset(
    [
        vk.VkUserPermissions.MESSAGES,
        vk.VkUserPermissions.PHOTOS,
        vk.VkUserPermissions.STATUS,
        vk.VkUserPermissions.VIDEO,
    ]
)
DEFAULT_DESTINATION_PATH = pathlib.Path(".") / "vk_fetch_downloads"

VK_MAX_ITEMS_COUNT = 200
VK_GROUP_PEER_ID_SINCE = 2000000000
KATE_MOBILE_APP_ID = 2685278


class DownloadStatus(enum.Enum):
    Success = enum.auto()
    Failed = enum.auto()


class MediaType(enum.Enum):
    Photo = "photo"
    Video = "video"
    Audio = "audio"
    Doc = "doc"
    Link = "link"
    Market = "market"
    Wall = "wall"
    Poll = "poll"
    Gift = "gift"
    Sticker = "sticker"


DEFAULT_CONVERSATION_MEDIA_TYPES = frozenset(MediaType)


class Sex(enum.Enum):
    Female = 1
    Male = 2
    Undefined = 0

    def __str__(self):
        match self:
            case Sex.Female:
                return "женский"
            case Sex.Male:
                return "мужской"
            case Sex.Undefined:
                return "не указан"


class Relation(enum.Enum):
    NotMarried = 1
    HasFriend = 2
    Engaged = 3
    Married = 4
    Complicated = 5
    InActiveSearch = 6
    InLove = 7
    CivilMarriage = 8
    Undefined = 0

    def __str__(self):
        match self:
            case Relation.NotMarried:
                return "не женат/не замужем"
            case Relation.HasFriend:
                return "есть друг/есть подруга"
            case Relation.Engaged:
                return "помолвлен/помолвлена"
            case Relation.Married:
                return "женат/замужем"
            case Relation.Complicated:
                return "всё сложно"
            case Relation.InActiveSearch:
                return "в активном поиске"
            case Relation.InLove:
                return "в гражданском браке"
            case Relation.Undefined:
                return "не указано"


class ConversationType(enum.Enum):
    User = "user"
    Chat = "chat"
    Group = "group"
    Email = "email"


class ConversationState(enum.Enum):
    In = "in"
    Kicked = "kicked"
    Left = "left"
