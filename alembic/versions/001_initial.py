"""Initial tables

Revision ID: 001_initial
Revises: 
Create Date: 2026-01-20 21:40:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create ENUM types
    op.execute("CREATE TYPE agentstatus AS ENUM ('active', 'inactive', 'archived')")
    op.execute("CREATE TYPE conversationstatus AS ENUM ('active', 'paused', 'closed')")
    op.execute("CREATE TYPE messagerole AS ENUM ('user', 'assistant', 'system')")
    
    # Create agents table
    op.create_table('agents',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('system_prompt', sa.Text(), nullable=False),
    sa.Column('model', sa.String(length=100), nullable=True),
    sa.Column('temperature', sa.Float(), nullable=True),
    sa.Column('rag_enabled', sa.Boolean(), nullable=True),
    sa.Column('whatsapp_enabled', sa.Boolean(), nullable=True),
    sa.Column('email_enabled', sa.Boolean(), nullable=True),
    sa.Column('status', postgresql.ENUM('active', 'inactive', 'archived', name='agentstatus'), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    
    # Create conversations table
    op.create_table('conversations',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('agent_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_identifier', sa.String(length=255), nullable=False),
    sa.Column('channel', sa.String(length=50), nullable=True),
    sa.Column('status', postgresql.ENUM('active', 'paused', 'closed', name='conversationstatus'), nullable=True),
    sa.Column('extra_data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['agent_id'], ['agents.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    
    # Create documents table
    op.create_table('documents',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('agent_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('filename', sa.String(length=255), nullable=False),
    sa.Column('file_type', sa.String(length=50), nullable=True),
    sa.Column('file_size', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.Column('chunks_count', sa.Integer(), nullable=True),
    sa.Column('extra_data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['agent_id'], ['agents.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    
    # Create channel_configs table
    op.create_table('channel_configs',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('agent_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('channel', sa.String(length=50), nullable=False),
    sa.Column('config', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('enabled', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['agent_id'], ['agents.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    
    # Create messages table
    op.create_table('messages',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('conversation_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('role', postgresql.ENUM('user', 'assistant', 'system', name='messagerole'), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('tokens', sa.Integer(), nullable=True),
    sa.Column('cost', sa.Float(), nullable=True),
    sa.Column('processing_time', sa.Float(), nullable=True),
    sa.Column('extra_data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('messages')
    op.drop_table('channel_configs')
    op.drop_table('documents')
    op.drop_table('conversations')
    op.drop_table('agents')
    op.execute('DROP TYPE messagerole')
    op.execute('DROP TYPE conversationstatus')
    op.execute('DROP TYPE agentstatus')
