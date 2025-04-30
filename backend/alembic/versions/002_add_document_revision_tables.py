"""Add document revision management tables

Revision ID: 002
Revises: 001
Create Date: 2025-04-30

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    # ドキュメントテーブルの作成
    op.create_table(
        'documents',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
    )
    op.create_index('idx_documents_title', 'documents', ['title'])

    # ドキュメントリビジョンテーブルの作成
    op.create_table(
        'document_revisions',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('document_id', UUID(as_uuid=True), sa.ForeignKey('documents.id', ondelete='CASCADE'), nullable=False),
        sa.Column('version', sa.String(20), nullable=False),
        sa.Column('storage_key', sa.String(255), nullable=False),
        sa.Column('change_summary', sa.Text()),
        sa.Column('created_by', UUID(as_uuid=True)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.UniqueConstraint('document_id', 'version', name='uq_document_revisions_document_id_version'),
    )
    op.create_index('idx_document_revisions_document_id', 'document_revisions', ['document_id'])

    # ノードとドキュメントの関連付けテーブルの作成
    op.create_table(
        'node_document_links',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('node_id', UUID(as_uuid=True), sa.ForeignKey('roadmap_nodes.id', ondelete='CASCADE'), nullable=False),
        sa.Column('document_id', UUID(as_uuid=True), sa.ForeignKey('documents.id', ondelete='CASCADE'), nullable=False),
        sa.Column('order_position', sa.Integer()),
        sa.Column('relation_type', sa.String(50), nullable=False, default='primary'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.UniqueConstraint('node_id', 'document_id', name='uq_node_document_links_node_id_document_id'),
    )
    op.create_index('idx_node_document_links_node_id', 'node_document_links', ['node_id'])
    op.create_index('idx_node_document_links_document_id', 'node_document_links', ['document_id'])


def downgrade():
    # 全てのテーブルを削除（依存関係の逆順）
    op.drop_table('node_document_links')
    op.drop_table('document_revisions')
    op.drop_table('documents')
