"""create initial schema

Revision ID: 001
Revises: 
Create Date: 2025-11-27 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create hospitals table
    op.create_table(
        'hospitals',
        sa.Column('hospital_id', sa.String(50), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('latitude', sa.Numeric(10, 8), nullable=True),
        sa.Column('longitude', sa.Numeric(11, 8), nullable=True),
        sa.Column('contact_name', sa.String(255), nullable=True),
        sa.Column('contact_phone', sa.String(20), nullable=True),
        sa.Column('contact_email', sa.String(255), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False)
    )

    # Create inventory table
    op.create_table(
        'inventory',
        sa.Column('record_id', sa.String(50), primary_key=True),
        sa.Column('hospital_id', sa.String(50), sa.ForeignKey('hospitals.hospital_id'), nullable=False),
        sa.Column('blood_group', sa.String(5), nullable=False),
        sa.Column('component', sa.String(20), nullable=False),
        sa.Column('units', sa.Integer(), nullable=False),
        sa.Column('unit_expiry_date', sa.Date(), nullable=False),
        sa.Column('collection_date', sa.Date(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.CheckConstraint("blood_group IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')", name='chk_blood_group'),
        sa.CheckConstraint("component IN ('RBC', 'Platelets', 'Plasma')", name='chk_component'),
        sa.CheckConstraint('units > 0', name='chk_units')
    )

    # Create usage table
    op.create_table(
        'usage',
        sa.Column('usage_id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('hospital_id', sa.String(50), sa.ForeignKey('hospitals.hospital_id'), nullable=False),
        sa.Column('blood_group', sa.String(5), nullable=False),
        sa.Column('component', sa.String(20), nullable=False),
        sa.Column('units_used', sa.Integer(), nullable=False),
        sa.Column('usage_date', sa.Date(), nullable=False),
        sa.Column('purpose', sa.String(50), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.CheckConstraint("purpose IN ('surgery', 'emergency', 'other')", name='chk_purpose')
    )

    # Create donors table
    op.create_table(
        'donors',
        sa.Column('donor_id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('email', sa.String(255), nullable=True),
        sa.Column('blood_group', sa.String(5), nullable=False),
        sa.Column('last_donation_date', sa.Date(), nullable=True),
        sa.Column('eligible', sa.Boolean(), server_default=sa.text('TRUE'), nullable=False),
        sa.Column('location_lat', sa.Numeric(10, 8), nullable=True),
        sa.Column('location_lon', sa.Numeric(11, 8), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False)
    )

    # Create forecasts table
    op.create_table(
        'forecasts',
        sa.Column('forecast_id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('hospital_id', sa.String(50), sa.ForeignKey('hospitals.hospital_id'), nullable=False),
        sa.Column('blood_group', sa.String(5), nullable=False),
        sa.Column('component', sa.String(20), nullable=False),
        sa.Column('forecast_date', sa.Date(), nullable=False),
        sa.Column('predicted_units', sa.Numeric(10, 2), nullable=False),
        sa.Column('lower_bound', sa.Numeric(10, 2), nullable=True),
        sa.Column('upper_bound', sa.Numeric(10, 2), nullable=True),
        sa.Column('generated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.UniqueConstraint('hospital_id', 'blood_group', 'component', 'forecast_date', 'generated_at', 
                          name='uq_forecast_unique')
    )

    # Create users table
    op.create_table(
        'users',
        sa.Column('user_id', sa.String(50), primary_key=True),
        sa.Column('username', sa.String(100), unique=True, nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('role', sa.String(20), nullable=False),
        sa.Column('hospital_id', sa.String(50), sa.ForeignKey('hospitals.hospital_id'), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.CheckConstraint("role IN ('staff', 'admin')", name='chk_role')
    )

    # Create transfers table
    op.create_table(
        'transfers',
        sa.Column('transfer_id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('source_hospital_id', sa.String(50), sa.ForeignKey('hospitals.hospital_id'), nullable=False),
        sa.Column('destination_hospital_id', sa.String(50), sa.ForeignKey('hospitals.hospital_id'), nullable=False),
        sa.Column('blood_group', sa.String(5), nullable=False),
        sa.Column('component', sa.String(20), nullable=False),
        sa.Column('units', sa.Integer(), nullable=False),
        sa.Column('urgency_score', sa.Numeric(5, 3), nullable=True),
        sa.Column('distance_km', sa.Numeric(6, 2), nullable=True),
        sa.Column('eta_minutes', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(20), server_default=sa.text("'pending'"), nullable=False),
        sa.Column('approved_by', sa.String(50), nullable=True),
        sa.Column('approved_at', sa.TIMESTAMP(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.CheckConstraint("status IN ('pending', 'approved', 'completed', 'cancelled')", name='chk_status')
    )

    # Create audit_logs table
    op.create_table(
        'audit_logs',
        sa.Column('log_id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.String(50), nullable=True),
        sa.Column('action', sa.String(100), nullable=False),
        sa.Column('resource_type', sa.String(50), nullable=True),
        sa.Column('resource_id', sa.String(50), nullable=True),
        sa.Column('details', postgresql.JSONB(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False)
    )

    # Create notifications table
    op.create_table(
        'notifications',
        sa.Column('notification_id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('donor_id', sa.Integer(), sa.ForeignKey('donors.donor_id'), nullable=True),
        sa.Column('template_id', sa.String(50), nullable=True),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('status', sa.String(20), server_default=sa.text("'pending'"), nullable=False),
        sa.Column('sent_at', sa.TIMESTAMP(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.CheckConstraint("status IN ('pending', 'sent', 'failed', 'simulated')", name='chk_notification_status')
    )

    # Create indexes for common query patterns
    op.create_index('idx_inventory_hospital', 'inventory', ['hospital_id'])
    op.create_index('idx_inventory_blood_group', 'inventory', ['blood_group'])
    op.create_index('idx_inventory_expiry', 'inventory', ['unit_expiry_date'])
    op.create_index('idx_usage_hospital_date', 'usage', ['hospital_id', 'usage_date'])
    op.create_index('idx_donors_blood_group', 'donors', ['blood_group'])
    op.create_index('idx_donors_eligible', 'donors', ['eligible'])
    op.create_index('idx_forecasts_hospital_date', 'forecasts', ['hospital_id', 'forecast_date'])
    op.create_index('idx_transfers_status', 'transfers', ['status'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('idx_transfers_status', table_name='transfers')
    op.drop_index('idx_forecasts_hospital_date', table_name='forecasts')
    op.drop_index('idx_donors_eligible', table_name='donors')
    op.drop_index('idx_donors_blood_group', table_name='donors')
    op.drop_index('idx_usage_hospital_date', table_name='usage')
    op.drop_index('idx_inventory_expiry', table_name='inventory')
    op.drop_index('idx_inventory_blood_group', table_name='inventory')
    op.drop_index('idx_inventory_hospital', table_name='inventory')

    # Drop tables in reverse order (respecting foreign key constraints)
    op.drop_table('notifications')
    op.drop_table('audit_logs')
    op.drop_table('transfers')
    op.drop_table('users')
    op.drop_table('forecasts')
    op.drop_table('donors')
    op.drop_table('usage')
    op.drop_table('inventory')
    op.drop_table('hospitals')
