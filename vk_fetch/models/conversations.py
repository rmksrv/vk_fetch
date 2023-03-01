import collections
import dataclasses as dc
import typing as t

from vk_fetch import constants, models, utils, fetchers, core


@dc.dataclass(frozen=True, slots=True)
class ConversationPeer:
    id: int
    type: constants.ConversationType
    local_id: int

    @classmethod
    def of(cls, d: dict[str, t.Any]) -> t.Self:
        return cls(
            type=constants.ConversationType(d.get("type")),
            **utils.keys_excluded_dict(d, ["type"]),
        )


@dc.dataclass(frozen=True, slots=True)
class ConversationPushSettings:
    no_sound: bool
    disabled_forever: bool
    disabled_mentions: bool
    disabled_mass_mentions: bool

    @classmethod
    @utils.none_on_throw(TypeError)
    def of(cls, d: dict[str, t.Any]) -> t.Self:
        return cls(**d)


@dc.dataclass(frozen=True, slots=True)
class ConversationCanWrite:
    allowed: bool
    reason: int | None = None

    @classmethod
    def of(cls, d: dict[str, t.Any]) -> t.Self:
        return cls(**d)


@dc.dataclass(frozen=True, slots=True)
class ConversationsChatSettingsPhoto:
    photo_50: str
    photo_100: str
    photo_200: str
    is_default_photo: bool
    is_default_call_photo: bool

    @classmethod
    @utils.none_on_throw(TypeError)
    def of(cls, d: dict[str, t.Any]) -> t.Self:
        return cls(**d)


@dc.dataclass(frozen=True, slots=True)
class ConversationsChatSettingsAcl:
    can_change_info: bool
    can_change_invite_link: bool
    can_change_pin: bool
    can_change_style: bool
    can_invite: bool
    can_promote_users: bool
    can_see_invite_link: bool
    can_moderate: bool
    can_copy_chat: bool
    can_use_mass_mentions: bool
    can_call: bool

    @classmethod
    def of(cls, d: dict[str, t.Any]) -> t.Self:
        return cls(**d)


@dc.dataclass(frozen=True, slots=True)
class ConversationChatSettings:
    title: str
    members_count: int
    owner_id: int
    state: constants.ConversationState
    photo: ConversationsChatSettingsPhoto
    active_ids: list[int]
    is_group_channel: bool
    acl: ConversationsChatSettingsAcl
    is_service: bool
    pinned_message: models.Message | None = None
    short_poll_reactions: bool | None = None

    @classmethod
    @utils.none_on_throw(AttributeError)
    def of(cls, d: dict[str, t.Any]) -> t.Self:
        exclude_fields = ["state", "photo", "acl", "pinned_message"]
        return cls(
            state=constants.ConversationState(d.get("state")),
            photo=ConversationsChatSettingsPhoto.of(d.get("photo")),
            acl=ConversationsChatSettingsAcl.of(d.get("acl")),
            pinned_message=models.Message.of(d.get("pinned_message")),
            **utils.keys_excluded_dict(d, exclude_fields),
        )

    def full_name(self) -> str:
        return self.title


@dc.dataclass(frozen=True, slots=True)
class Conversation:
    peer: ConversationPeer
    last_message_id: int
    in_read: int
    out_read: int
    last_conversation_message_id: int
    in_read_cmid: int
    out_read_cmid: int
    is_marked_unread: bool
    important: bool
    can_write: ConversationCanWrite
    style: str | None = None
    unread_count: int | None = None
    push_settings: ConversationPushSettings | None = None
    chat_settings: ConversationChatSettings | None = None

    @classmethod
    def of(cls, d: dict[str, t.Any]) -> t.Self:
        exclude_fields = [
            "peer",
            "push_settings",
            "can_write",
            "chat_settings",
            "current_keyboard",
        ]
        return cls(
            peer=ConversationPeer.of(d.get("peer")),
            push_settings=ConversationPushSettings.of(d.get("push_settings")),
            can_write=ConversationCanWrite.of(d.get("can_write")),
            chat_settings=ConversationChatSettings.of(d.get("chat_settings")),
            **utils.keys_excluded_dict(d, exclude_fields),
        )


PeerInfoType = models.User | ConversationChatSettings


@dc.dataclass(frozen=True, slots=True)
class ConversationItem:
    conversation: Conversation
    last_message: models.Message

    @classmethod
    def of(cls, d: dict[str, t.Any]) -> t.Self:
        return cls(
            conversation=Conversation.of(d.get("conversation")),
            last_message=models.Message.of(d.get("last_message")),
        )

    def peer_info(self, api: core.APIProvider) -> PeerInfoType:
        match self.conversation.peer.type:
            case constants.ConversationType.User:
                return fetchers.users(api, [self.conversation.peer.id])[0]
            case constants.ConversationType.Chat:
                return self.conversation.chat_settings
            case _:
                raise NotImplemented


class ConversationItemList(collections.UserList[ConversationItem]):
    def peer_ids(self) -> list[int]:
        return [item.conversation.peer.id for item in self]

    def peer_infos(
        self, api: core.APIProvider
    ) -> dict[constants.ConversationType, list[PeerInfoType]]:
        user_ids = [
            item.conversation.peer.id
            for item in self
            if item.conversation.peer.type is constants.ConversationType.User
        ]
        chat_infos = [
            item.peer_info(api)
            for item in self
            if item.conversation.peer.type is constants.ConversationType.Chat
        ]
        group_ids = [
            item.conversation.peer.id
            for item in self
            if item.conversation.peer.type is constants.ConversationType.Group
        ]
        email_ids = [
            item.conversation.peer.id
            for item in self
            if item.conversation.peer.type is constants.ConversationType.Email
        ]
        return {
            constants.ConversationType.User: fetchers.users(api, user_ids),
            constants.ConversationType.Chat: chat_infos,
            constants.ConversationType.Group: group_ids,
            constants.ConversationType.Email: email_ids,
        }

    def excluded_peers(
        self, exclude_peers: t.Iterable[str] = frozenset()
    ) -> t.Self:
        exclude_peers = [utils.peer_id_from_sel(sel) for sel in exclude_peers]

        def _is_peer_to_exclude(item: models.ConversationItem) -> bool:
            return item.conversation.peer.id not in exclude_peers

        return self.__class__(filter(_is_peer_to_exclude, self))
