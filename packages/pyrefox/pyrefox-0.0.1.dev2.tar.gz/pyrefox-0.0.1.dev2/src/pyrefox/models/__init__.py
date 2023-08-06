from typing import Optional, Union

from ..types import (
    Model, Object,
    AnyUrl, AboutUri, FileUri, HttpUrl, ResourceUri, MozExtensionUri, ViewSourceAnyUrl,
    datetime, date,
)
from ..utils import _camel
from .enums import (
    BookmarkType,
    EventType,
    PermissionType,
    SameSite,
    SpecialGuid,
    SyncStatus,
)
from .extensions import AddOnsStartUp, Extensions


class Bookmark(Model):
    '''
    Attrs:
        index: position in the parent folder.
    '''
    id:                  int
    type:                BookmarkType
    fk:                  Optional[int]
    parent:              int
    position:            int
    title:               Optional[str]
    keyword_id:          Optional[int]
    folder_type:         Optional[str]
    date_added:          datetime
    last_modified:       datetime
    guid:                Union[SpecialGuid, str]  # TODO: len == 12
    sync_status:         SyncStatus
    sync_change_counter: int

    class Config:
        orm_mode = True


class Place(Model):
    id:                int
    url:               AnyUrl
    title:             str
    rev_host:          str
    visit_count:       int
    hidden:            int
    typed:             int
    frecency:          int
    last_visit_date:   int
    guid:              str
    foreign_count:     int
    url_hash:          int
    description:       str
    preview_image_url: AnyUrl
    origin_id:         int


class SearchEngine(Model):
    name:            str
    is_app_provided: bool
    meta_data:       Object

    class Config:
        alias_generator = _camel
        extra = 'allow'


class SearchEngines(Model):
    version:   int
    engines:   list[SearchEngine]
    meta_data: Object  # TODO


class Event(Model):
    id:        int
    type:      EventType
    count:     int
    timestamp: date


class Permission(Model):
    id:                int
    origin:            Union[HttpUrl, AboutUri, FileUri, ResourceUri, MozExtensionUri, ViewSourceAnyUrl]
    type:              PermissionType
    permission:        bool
    expire_type:       int
    expire_time:       datetime
    modification_time: datetime


class Cookie(Model):
    id:                 int
    origin_attributes:  str
    name:               str
    value:              str
    host:               str
    path:               str
    expiry:             datetime
    last_accessed:      datetime
    creation_time:      datetime
    is_secure:          bool
    is_http_only:       bool
    in_browser_element: bool
    same_site:          SameSite
    raw_same_site:      SameSite
    scheme_map:         int


__all__ = [
    'AddOnsStartUp',
    'Event',
    'Extensions',
]
