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
"""add tenant info to users

Revision ID: ecd71d5ff1b9
Revises: ffa79af61a56
Create Date: 2022-08-16 11:49:26.118790

"""

# revision identifiers, used by Alembic.
revision = 'ecd71d5ff1b9'
down_revision = 'ffa79af61a56'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column("ab_user", sa.Column("travel_id", sa.BigInteger(), nullable=False))
    op.add_column("ab_user", sa.Column("travel_name", sa.String(255), nullable=False))
    op.add_column("ab_user", sa.Column("user_type", sa.String(64), nullable=False))
    op.add_column("ab_user", sa.Column("user_role", sa.String(64), nullable=False))


def downgrade():
    op.drop_column("ab_user", "travel_id")
    op.drop_column("ab_user", "travel_name")
    op.drop_column("ab_user", "user_type")
    op.drop_column("ab_user", "user_role")
