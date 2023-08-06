from ._sql import (
    Column, ForeignKey, Index, UniqueConstraint, PrimaryKeyConstraint,
    declarative_base, relationship, now, text,
)
from ._types import Integer, NullType, String, Text, UnixTimeMicro

PlacesBase = declarative_base()


class AnnotationAttributeOrm(PlacesBase):
    __tablename__ = 'moz_anno_attributes'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)


class AnnotationOrm(PlacesBase):
    __tablename__ = 'moz_annos'
    __table_args__ = Index('moz_annos_placeattributeindex',
                           'place_id',
                           'anno_attribute_id',
                           unique=True),

    id = Column(Integer, primary_key=True)
    place_id = Column(Integer, nullable=False)
    anno_attribute_id = Column(Integer)
    content = Column(Text)
    flags = Column(Integer, server_default=text('0'))
    expiration = Column(Integer, server_default=text('0'))
    type = Column(Integer, server_default=text('0'))
    dateAdded = Column(UnixTimeMicro, server_default=now())
    lastModified = Column(UnixTimeMicro, server_default=now())


class BookmarkOrm(PlacesBase):
    __tablename__ = 'moz_bookmarks'
    __table_args__ = (
        Index('moz_bookmarks_itemindex', 'fk', 'type'),
        Index('moz_bookmarks_parentindex', 'parent', 'position'),
        Index('moz_bookmarks_itemlastmodifiedindex', 'fk', 'lastModified'),
    )

    id = Column(Integer, primary_key=True)
    type = Column(Integer)
    fk = Column(Integer, server_default=text('NULL'))
    parent = Column(Integer, nullable=False)
    position = Column(Integer)
    title = Column(Text)
    keyword_id = Column(Integer)
    folder_type = Column(Text)
    dateAdded = Column(UnixTimeMicro, index=True)
    lastModified = Column(UnixTimeMicro)
    guid = Column(String(12), unique=True)
    syncStatus = Column(Integer, nullable=False, server_default=text('0'))
    syncChangeCounter = Column(Integer, nullable=False, server_default=text('1'))


class BookmarksDeletedOrm(PlacesBase):
    __tablename__ = 'moz_bookmarks_deleted'

    guid = Column(Text, primary_key=True)
    dateRemoved = Column(Integer, nullable=False, server_default=text('0'))


class HistoryVisitOrm(PlacesBase):
    __tablename__ = 'moz_historyvisits'
    __table_args__ = Index('moz_historyvisits_placedateindex',
                           'place_id',
                           'visit_date'),

    id = Column(Integer, primary_key=True)
    from_visit = Column(Integer, index=True)
    place_id = Column(Integer)
    visit_date = Column(Integer, index=True)
    visit_type = Column(Integer)
    session = Column(Integer)


class InputHistoryOrm(PlacesBase):
    __tablename__ = 'moz_inputhistory'

    place_id = Column(Integer, primary_key=True, nullable=False)
    input = Column(Text, primary_key=True, nullable=False)
    use_count = Column(Integer)


class ItemAnnotationOrm(PlacesBase):
    __tablename__ = 'moz_items_annos'
    __table_args__ = Index('moz_items_annos_itemattributeindex',
                           'item_id',
                           'anno_attribute_id',
                           unique=True),

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, nullable=False)
    anno_attribute_id = Column(Integer)
    content = Column(Text)
    flags = Column(Integer, server_default=text('0'))
    expiration = Column(Integer, server_default=text('0'))
    type = Column(Integer, server_default=text('0'))
    dateAdded = Column(Integer, server_default=text('0'))
    lastModified = Column(Integer, server_default=text('0'))


class KeywordOrm(PlacesBase):
    __tablename__ = 'moz_keywords'
    __table_args__ = Index('moz_keywords_placepostdata_uniqueindex',
                           'place_id',
                           'post_data',
                           unique=True),

    id = Column(Integer, primary_key=True)
    keyword = Column(Text, unique=True)
    place_id = Column(Integer)
    post_data = Column(Text)


class MetaOrm(PlacesBase):
    __tablename__ = 'moz_meta'

    key = Column(Text, primary_key=True)
    value = Column(NullType, nullable=False)


class OriginOrm(PlacesBase):
    __tablename__ = 'moz_origins'
    __table_args__ = UniqueConstraint('prefix', 'host'),

    id = Column(Integer, primary_key=True)
    prefix = Column(Text, nullable=False)
    host = Column(Text, nullable=False)
    frecency = Column(Integer, nullable=False)


class PlaceOrm(PlacesBase):
    __tablename__ = 'moz_places'

    id = Column(Integer, primary_key=True)
    url = Column(Text)
    title = Column(Text)
    rev_host = Column(Text, index=True)
    visit_count = Column(Integer, index=True, server_default=text('0'))
    hidden = Column(Integer, nullable=False, server_default=text('0'))
    typed = Column(Integer, nullable=False, server_default=text('0'))
    frecency = Column(Integer, nullable=False, index=True, server_default=text('-1'))
    last_visit_date = Column(Integer, index=True)
    guid = Column(Text, unique=True)
    foreign_count = Column(Integer, nullable=False, server_default=text('0'))
    url_hash = Column(Integer, nullable=False, index=True, server_default=text('0'))
    description = Column(Text)
    preview_image_url = Column(Text)
    origin_id = Column(ForeignKey('moz_origins.id'), index=True)

    origin = relationship('OriginOrm')


class Sequence(PlacesBase):
    __tablename__ = 'sqlite_sequence'
    __table_args__ = PrimaryKeyConstraint('name', 'seq'),

    name = Column(NullType)
    seq = Column(NullType)


class Stat(PlacesBase):
    __tablename__ = 'sqlite_stat1'
    __table_args__ = PrimaryKeyConstraint('tbl', 'idx', 'stat'),

    tbl = Column(NullType)
    idx = Column(NullType)
    stat = Column(NullType)
