"""create tables

Revision ID: 35786620c58a
Revises: 
Create Date: 2023-12-08 22:52:36.447753

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '35786620c58a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_table('users_roles',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.Enum('USER', 'MANAGER', 'SUPERVISOR', 'ANALYST', 'TESTER', 'EXECUTOR', 'ADMIN', name='roles'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users_logins',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('login_at', sa.DateTime(), nullable=False),
    sa.Column('ip_address', sa.String(length=50), nullable=False),
    sa.Column('user_agent', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users_roles_map',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('role_name', sa.Enum('USER', 'MANAGER', 'SUPERVISOR', 'ANALYST', 'TESTER', 'EXECUTOR', 'ADMIN', name='roles'), nullable=False),
    sa.ForeignKeyConstraint(['role_name'], ['users_roles.name'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'role_name')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_roles_map')
    op.drop_table('users_logins')
    op.drop_table('users_roles')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
