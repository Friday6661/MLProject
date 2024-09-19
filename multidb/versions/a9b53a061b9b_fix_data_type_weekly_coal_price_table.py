"""Fix Data type Weekly Coal Price Table

Revision ID: a9b53a061b9b
Revises: 4f0ea937824f
Create Date: 2024-09-12 17:38:03.196444

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9b53a061b9b'
down_revision: Union[str, None] = '4f0ea937824f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade(engine_name: str) -> None:
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name: str) -> None:
    globals()["downgrade_%s" % engine_name]()





def upgrade_engine1() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_M_KOMTRAX_id', table_name='M_KOMTRAX')
    op.drop_table('M_KOMTRAX')
    op.drop_index('ix_T_COALPRICE_id', table_name='T_COALPRICE')
    op.drop_table('T_COALPRICE')
    op.drop_index('ix_M_WEEKLYCOALPRICE_id', table_name='M_WEEKLYCOALPRICE')
    op.drop_table('M_WEEKLYCOALPRICE')
    op.drop_index('ix_M_MONTHLYSALES_id', table_name='M_MONTHLYSALES')
    op.drop_table('M_MONTHLYSALES')
    op.drop_index('ix_M_MONTHLYSTOCKS_id', table_name='M_MONTHLYSTOCKS')
    op.drop_table('M_MONTHLYSTOCKS')
    # ### end Alembic commands ###


def downgrade_engine1() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('M_MONTHLYSTOCKS',
    sa.Column('id', sa.INTEGER(), sa.Identity(always=False, start=1, increment=1), autoincrement=True, nullable=False),
    sa.Column('gr', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('model', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('model_spec', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('sn', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('stat', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('loc', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('aging', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('sm_b', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='PK__M_MONTHL__3213E83F5972643C')
    )
    op.create_index('ix_M_MONTHLYSTOCKS_id', 'M_MONTHLYSTOCKS', ['id'], unique=False)
    op.create_table('M_MONTHLYSALES',
    sa.Column('id', sa.INTEGER(), sa.Identity(always=False, start=1, increment=1), autoincrement=True, nullable=False),
    sa.Column('customer_name', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('sec', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('gr', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('model', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('model_spec', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('sn', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('loc', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('billing', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('sm_b', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('gov_soe', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='PK__M_MONTHL__3213E83FE4352A76')
    )
    op.create_index('ix_M_MONTHLYSALES_id', 'M_MONTHLYSALES', ['id'], unique=False)
    op.create_table('M_WEEKLYCOALPRICE',
    sa.Column('id', sa.INTEGER(), sa.Identity(always=False, start=1, increment=1), autoincrement=True, nullable=False),
    sa.Column('date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('trade_region_and_specification', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('trade_terms', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('price', sa.DECIMAL(precision=18, scale=0), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='PK__M_WEEKLY__3213E83F797215E6')
    )
    op.create_index('ix_M_WEEKLYCOALPRICE_id', 'M_WEEKLYCOALPRICE', ['id'], unique=False)
    op.create_table('T_COALPRICE',
    sa.Column('id', sa.INTEGER(), sa.Identity(always=False, start=1, increment=1), autoincrement=True, nullable=False),
    sa.Column('date', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('price_per_ton', sa.DECIMAL(precision=12, scale=2), autoincrement=False, nullable=False),
    sa.Column('currency', sa.VARCHAR(length=10, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('location', sa.VARCHAR(length=100, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('grade', sa.VARCHAR(length=50, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('supplier', sa.VARCHAR(length=100, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('notes', sa.VARCHAR(length=255, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='PK__T_COALPR__3213E83F5FF9210C')
    )
    op.create_index('ix_T_COALPRICE_id', 'T_COALPRICE', ['id'], unique=False)
    op.create_table('M_KOMTRAX',
    sa.Column('id', sa.INTEGER(), sa.Identity(always=False, start=1, increment=1), autoincrement=True, nullable=False),
    sa.Column('year', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('month', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('model', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('type', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('serial_number', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('customer_name', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('current_smr', sa.DECIMAL(precision=10, scale=2), autoincrement=False, nullable=True),
    sa.Column('current_smr_time', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('sum_monthly_working_hours', sa.DECIMAL(precision=10, scale=2), autoincrement=False, nullable=True),
    sa.Column('sum_monthly_working_days', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='PK__M_KOMTRA__3213E83F98FBC7C1')
    )
    op.create_index('ix_M_KOMTRAX_id', 'M_KOMTRAX', ['id'], unique=False)
    # ### end Alembic commands ###


def upgrade_engine2() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_T_COALPRICECLEAN_id', table_name='T_COALPRICECLEAN')
    op.drop_table('T_COALPRICECLEAN')
    op.drop_index('ix_T_KOMTRAXCLEAN_id', table_name='T_KOMTRAXCLEAN')
    op.drop_table('T_KOMTRAXCLEAN')
    op.drop_index('ix_T_MONTHLYSALESCLEAN_id', table_name='T_MONTHLYSALESCLEAN')
    op.drop_table('T_MONTHLYSALESCLEAN')
    op.drop_index('ix_T_MONTHLYSTOCKSCLEAN_id', table_name='T_MONTHLYSTOCKSCLEAN')
    op.drop_table('T_MONTHLYSTOCKSCLEAN')
    # ### end Alembic commands ###


def downgrade_engine2() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('T_MONTHLYSTOCKSCLEAN',
    sa.Column('id', sa.INTEGER(), sa.Identity(always=False, start=1, increment=1), autoincrement=True, nullable=False),
    sa.Column('gr', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('model', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('model_spec', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('sn', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('stat', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('loc', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('aging', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('sm_b', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='PK__T_MONTHL__3213E83F020ADD88')
    )
    op.create_index('ix_T_MONTHLYSTOCKSCLEAN_id', 'T_MONTHLYSTOCKSCLEAN', ['id'], unique=False)
    op.create_table('T_MONTHLYSALESCLEAN',
    sa.Column('id', sa.INTEGER(), sa.Identity(always=False, start=1, increment=1), autoincrement=True, nullable=False),
    sa.Column('customer_name', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('sec', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('gr', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('model', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('model_spec', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('sn', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('loc', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('billing', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('sm_b', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('gov_soe', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='PK__T_MONTHL__3213E83FCC89F311')
    )
    op.create_index('ix_T_MONTHLYSALESCLEAN_id', 'T_MONTHLYSALESCLEAN', ['id'], unique=False)
    op.create_table('T_KOMTRAXCLEAN',
    sa.Column('id', sa.INTEGER(), sa.Identity(always=False, start=1, increment=1), autoincrement=True, nullable=False),
    sa.Column('year', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('month', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('model', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('type', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('serial_number', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('customer_name', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('current_smr', sa.DECIMAL(precision=10, scale=2), autoincrement=False, nullable=True),
    sa.Column('current_smr_time', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('sum_monthly_working_hours', sa.DECIMAL(precision=10, scale=2), autoincrement=False, nullable=True),
    sa.Column('sum_monthly_working_days', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='PK__T_KOMTRA__3213E83FDE98DBDC')
    )
    op.create_index('ix_T_KOMTRAXCLEAN_id', 'T_KOMTRAXCLEAN', ['id'], unique=False)
    op.create_table('T_COALPRICECLEAN',
    sa.Column('id', sa.INTEGER(), sa.Identity(always=False, start=1, increment=1), autoincrement=True, nullable=False),
    sa.Column('date', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('price_per_ton', sa.DECIMAL(precision=12, scale=2), autoincrement=False, nullable=False),
    sa.Column('currency', sa.VARCHAR(length=10, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('location', sa.VARCHAR(length=100, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('grade', sa.VARCHAR(length=50, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('supplier', sa.VARCHAR(length=100, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('notes', sa.VARCHAR(length=255, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='PK__T_COALPR__3213E83FF0EFD156')
    )
    op.create_index('ix_T_COALPRICECLEAN_id', 'T_COALPRICECLEAN', ['id'], unique=False)
    # ### end Alembic commands ###

