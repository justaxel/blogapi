import sqlalchemy


metadata = sqlalchemy.MetaData()

tbl_author = sqlalchemy.Table(
    'author', metadata,
    sqlalchemy.Column('id'),
    sqlalchemy.Column('username'),
    sqlalchemy.Column('email'),
    sqlalchemy.Column('status_account'),
    sqlalchemy.Column('password')
)