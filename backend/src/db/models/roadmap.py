import uuid
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, Float, Boolean, JSON, Text, DateTime, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..base import Base


class Category(Base):
    __tablename__ = 'categories'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), nullable=False, unique=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    order_index = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)

    # リレーションシップ
    themes = relationship('Theme', back_populates='category', cascade='all, delete-orphan')

    # インデックス
    __table_args__ = (
        Index('idx_categories_code', code),
        Index('idx_categories_is_active', is_active),
    )


class Theme(Base):
    __tablename__ = 'themes'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_id = Column(UUID(as_uuid=True), ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)
    code = Column(String(50), nullable=False, unique=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    order_index = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)

    # リレーションシップ
    category = relationship('Category', back_populates='themes')
    roadmaps = relationship('Roadmap', back_populates='theme', cascade='all, delete-orphan')

    # インデックス
    __table_args__ = (
        Index('idx_themes_category_id', category_id),
        Index('idx_themes_code', code),
        Index('idx_themes_is_active', is_active),
    )


class Roadmap(Base):
    __tablename__ = 'roadmaps'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    theme_id = Column(UUID(as_uuid=True), ForeignKey('themes.id', ondelete='CASCADE'), nullable=False)
    version = Column(String(20), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    is_published = Column(Boolean, default=False)
    is_latest = Column(Boolean, default=True)
    published_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)

    # リレーションシップ
    theme = relationship('Theme', back_populates='roadmaps')
    nodes = relationship('RoadmapNode', back_populates='roadmap', cascade='all, delete-orphan')
    edges = relationship('RoadmapEdge', back_populates='roadmap', cascade='all, delete-orphan')

    # インデックス・制約
    __table_args__ = (
        UniqueConstraint('theme_id', 'version', name='uq_roadmaps_theme_id_version'),
        Index('idx_roadmaps_theme_id', theme_id),
        Index('idx_roadmaps_is_published', is_published),
        Index('idx_roadmaps_is_latest', is_latest),
    )


class RoadmapNode(Base):
    __tablename__ = 'roadmap_nodes'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    roadmap_id = Column(UUID(as_uuid=True), ForeignKey('roadmaps.id', ondelete='CASCADE'), nullable=False)
    handle = Column(String(50), nullable=False)  # ノードの一意の識別子
    node_type = Column(String(50), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    position_x = Column(Float, nullable=False, default=0)
    position_y = Column(Float, nullable=False, default=0)
    meta_data = Column(JSON, nullable=False, default=dict)
    is_required = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)

    # リレーションシップ
    roadmap = relationship('Roadmap', back_populates='nodes')
    outgoing_edges = relationship('RoadmapEdge', foreign_keys='RoadmapEdge.source_node_id', back_populates='source_node')
    incoming_edges = relationship('RoadmapEdge', foreign_keys='RoadmapEdge.target_node_id', back_populates='target_node')

    # インデックス・制約
    __table_args__ = (
        UniqueConstraint('roadmap_id', 'handle', name='uq_roadmap_nodes_roadmap_id_handle'),
        Index('idx_roadmap_nodes_roadmap_id', roadmap_id),
        Index('idx_roadmap_nodes_node_type', node_type),
    )


class RoadmapEdge(Base):
    __tablename__ = 'roadmap_edges'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    roadmap_id = Column(UUID(as_uuid=True), ForeignKey('roadmaps.id', ondelete='CASCADE'), nullable=False)
    handle = Column(String(50), nullable=False)  # エッジの一意の識別子
    source_node_id = Column(UUID(as_uuid=True), ForeignKey('roadmap_nodes.id', ondelete='CASCADE'), nullable=False)
    target_node_id = Column(UUID(as_uuid=True), ForeignKey('roadmap_nodes.id', ondelete='CASCADE'), nullable=False)
    edge_type = Column(String(50), nullable=False, default='default')
    source_handle = Column(String(20))  # 接続元のポイント (top, right, bottom, left)
    target_handle = Column(String(20))  # 接続先のポイント (top, right, bottom, left)
    meta_data = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)

    # リレーションシップ
    roadmap = relationship('Roadmap', back_populates='edges')
    source_node = relationship('RoadmapNode', foreign_keys=[source_node_id], back_populates='outgoing_edges')
    target_node = relationship('RoadmapNode', foreign_keys=[target_node_id], back_populates='incoming_edges')

    # インデックス・制約
    __table_args__ = (
        UniqueConstraint('roadmap_id', 'handle', name='uq_roadmap_edges_roadmap_id_handle'),
        Index('idx_roadmap_edges_roadmap_id', roadmap_id),
        Index('idx_roadmap_edges_source_node_id', source_node_id),
        Index('idx_roadmap_edges_target_node_id', target_node_id),
        Index('idx_roadmap_edges_edge_type', edge_type),
    )
