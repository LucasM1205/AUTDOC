"""Add Benutzer table

Revision ID: de5bbaba7a1d
Revises: fc665cde6a72
Create Date: 2024-12-07 10:32:45.503140

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'de5bbaba7a1d'
down_revision = 'fc665cde6a72'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Tabelle 'benutzer' erstellen
    op.create_table(
        'benutzer',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('rolle', sa.String(), nullable=False),  # Rolle: Student, Sekretariat, etc.
        sa.Column('passwort', sa.String(), nullable=False),  # Gehashtes Passwort
        sa.Column('erstellt_am', sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    # Tabelle 'benutzer' entfernen
    op.drop_table('benutzer')
