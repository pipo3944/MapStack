"""Create roadmap related tables

Revision ID: 001
Revises:
Create Date: 2025-04-13

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # カテゴリテーブルの作成
    op.create_table(
        'categories',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('code', sa.String(50), nullable=False, unique=True),
        sa.Column('title', sa.String(100), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('order_index', sa.Float(), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
    )
    op.create_index('idx_categories_code', 'categories', ['code'])
    op.create_index('idx_categories_is_active', 'categories', ['is_active'])

    # テーマテーブルの作成
    op.create_table(
        'themes',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('category_id', UUID(as_uuid=True), sa.ForeignKey('categories.id', ondelete='CASCADE'), nullable=False),
        sa.Column('code', sa.String(50), nullable=False, unique=True),
        sa.Column('title', sa.String(100), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('order_index', sa.Float(), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
    )
    op.create_index('idx_themes_category_id', 'themes', ['category_id'])
    op.create_index('idx_themes_code', 'themes', ['code'])
    op.create_index('idx_themes_is_active', 'themes', ['is_active'])

    # ロードマップテーブルの作成
    op.create_table(
        'roadmaps',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('theme_id', UUID(as_uuid=True), sa.ForeignKey('themes.id', ondelete='CASCADE'), nullable=False),
        sa.Column('version', sa.String(20), nullable=False),
        sa.Column('title', sa.String(100), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('is_published', sa.Boolean(), default=False),
        sa.Column('is_latest', sa.Boolean(), default=True),
        sa.Column('published_at', sa.DateTime(timezone=True)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.UniqueConstraint('theme_id', 'version', name='uq_roadmaps_theme_id_version'),
    )
    op.create_index('idx_roadmaps_theme_id', 'roadmaps', ['theme_id'])
    op.create_index('idx_roadmaps_is_published', 'roadmaps', ['is_published'])
    op.create_index('idx_roadmaps_is_latest', 'roadmaps', ['is_latest'])

    # ロードマップノードテーブルの作成
    op.create_table(
        'roadmap_nodes',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('roadmap_id', UUID(as_uuid=True), sa.ForeignKey('roadmaps.id', ondelete='CASCADE'), nullable=False),
        sa.Column('handle', sa.String(50), nullable=False),
        sa.Column('node_type', sa.String(50), nullable=False),
        sa.Column('title', sa.String(100), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('position_x', sa.Float(), nullable=False, default=0),
        sa.Column('position_y', sa.Float(), nullable=False, default=0),
        sa.Column('meta_data', sa.JSON()),
        sa.Column('is_required', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.UniqueConstraint('roadmap_id', 'handle', name='uq_roadmap_nodes_roadmap_id_handle'),
    )
    op.create_index('idx_roadmap_nodes_roadmap_id', 'roadmap_nodes', ['roadmap_id'])
    op.create_index('idx_roadmap_nodes_node_type', 'roadmap_nodes', ['node_type'])

    # ロードマップエッジテーブルの作成
    op.create_table(
        'roadmap_edges',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('roadmap_id', UUID(as_uuid=True), sa.ForeignKey('roadmaps.id', ondelete='CASCADE'), nullable=False),
        sa.Column('handle', sa.String(50), nullable=False),
        sa.Column('source_node_id', UUID(as_uuid=True), sa.ForeignKey('roadmap_nodes.id', ondelete='CASCADE'), nullable=False),
        sa.Column('target_node_id', UUID(as_uuid=True), sa.ForeignKey('roadmap_nodes.id', ondelete='CASCADE'), nullable=False),
        sa.Column('edge_type', sa.String(50), nullable=False, default='default'),
        sa.Column('label', sa.String(100)),
        sa.Column('source_handle', sa.String(20)),
        sa.Column('target_handle', sa.String(20)),
        sa.Column('meta_data', sa.JSON()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.UniqueConstraint('roadmap_id', 'handle', name='uq_roadmap_edges_roadmap_id_handle'),
    )
    op.create_index('idx_roadmap_edges_roadmap_id', 'roadmap_edges', ['roadmap_id'])
    op.create_index('idx_roadmap_edges_source_node_id', 'roadmap_edges', ['source_node_id'])
    op.create_index('idx_roadmap_edges_target_node_id', 'roadmap_edges', ['target_node_id'])
    op.create_index('idx_roadmap_edges_edge_type', 'roadmap_edges', ['edge_type'])


def downgrade():
    # 全てのテーブルを削除（依存関係の逆順）
    op.drop_table('roadmap_edges')
    op.drop_table('roadmap_nodes')
    op.drop_table('roadmaps')
    op.drop_table('themes')
    op.drop_table('categories')
