import uuid
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, Integer, Text, DateTime, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..base import Base


class Document(Base):
    __tablename__ = 'documents'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)

    # リレーションシップ
    revisions = relationship('DocumentRevision', back_populates='document', cascade='all, delete-orphan')
    node_links = relationship('NodeDocumentLink', back_populates='document', cascade='all, delete-orphan')

    # インデックス
    __table_args__ = (
        Index('idx_documents_title', title),
    )


class DocumentRevision(Base):
    __tablename__ = 'document_revisions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey('documents.id', ondelete='CASCADE'), nullable=False)
    version = Column(String(20), nullable=False)
    storage_key = Column(String(255), nullable=False)
    change_summary = Column(Text)
    created_by = Column(UUID(as_uuid=True))
    created_at = Column(DateTime(timezone=True), default=datetime.now)

    # リレーションシップ
    document = relationship('Document', back_populates='revisions')

    # インデックス・制約
    __table_args__ = (
        UniqueConstraint('document_id', 'version', name='uq_document_revisions_document_id_version'),
        Index('idx_document_revisions_document_id', document_id),
    )


class NodeDocumentLink(Base):
    __tablename__ = 'node_document_links'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    node_id = Column(UUID(as_uuid=True), ForeignKey('roadmap_nodes.id', ondelete='CASCADE'), nullable=False)
    document_id = Column(UUID(as_uuid=True), ForeignKey('documents.id', ondelete='CASCADE'), nullable=False)
    order_position = Column(Integer)
    relation_type = Column(String(50), nullable=False, default='primary')
    created_at = Column(DateTime(timezone=True), default=datetime.now)

    # リレーションシップ
    node = relationship('RoadmapNode', back_populates='document_links')
    document = relationship('Document', back_populates='node_links')

    # インデックス・制約
    __table_args__ = (
        UniqueConstraint('node_id', 'document_id', name='uq_node_document_links_node_id_document_id'),
        Index('idx_node_document_links_node_id', node_id),
        Index('idx_node_document_links_document_id', document_id),
    )
