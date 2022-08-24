# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""add oauth config table

Revision ID: b68e9c72f5c0
Revises: ecd71d5ff1b9
Create Date: 2022-08-24 15:30:25.879983

"""

# revision identifiers, used by Alembic.
revision = 'b68e9c72f5c0'
down_revision = 'ecd71d5ff1b9'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        "oauth_configs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(256), nullable=False),
        sa.Column("token_key", sa.String(256), nullable=False),
        sa.Column("client_id", sa.String(256), nullable=False),
        sa.Column("client_secret", sa.String(256), nullable=False),
        sa.Column("api_base_url", sa.String(256), nullable=False),
        sa.Column("access_token_url", sa.String(256), nullable=False),
        sa.Column("authorize_url", sa.String(256), nullable=False),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("changed_on", sa.DateTime(), nullable=True),
        sa.Column("changed_by_fk", sa.Integer(), nullable=True),
        sa.Column("created_by_fk", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["changed_by_fk"], ["ab_user.id"]),
        sa.ForeignKeyConstraint(["created_by_fk"], ["ab_user.id"]),
    )


def downgrade():
    op.drop_table("oauth_configs")
