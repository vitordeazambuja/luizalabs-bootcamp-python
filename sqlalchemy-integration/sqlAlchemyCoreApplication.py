from sqlalchemy import (
    create_engine, MetaData, Table, Column,
    Integer, String, ForeignKey, text
)

engine = create_engine('sqlite:///:memory:', echo=False)

metadata_obj = MetaData()

user = Table(
    'user',
    metadata_obj,
    Column('user_id', Integer, primary_key=True),
    Column('user_name', String(40), nullable=False),
    Column('email_address', String(50)),
    Column('nickname', String(50), nullable=False)
)

user_prefs = Table(
    'user_prefs',
    metadata_obj,
    Column('pref_id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('user.user_id'), nullable=False),
    Column('pref_name', String(40)),
    Column('pref_value', String(100))
)

metadata_obj.create_all(engine)

with engine.connect() as conn:
    sql_insert = text("""
        INSERT INTO user (user_id, user_name, email_address, nickname)
        VALUES (:id, :name, :email, :nick)
    """)
    conn.execute(sql_insert, {
        "id": 2,
        "name": "maria",
        "email": "email@email.com",
        "nick": "ma"
    })

    conn.commit()

    print("\nExecutando SELECT")
    sql_select = text("SELECT * FROM user")
    result = conn.execute(sql_select)

    for row in result:
        print(row)

print("\nInfo da tabela user_prefs")
print(user_prefs.primary_key)
print(user_prefs.constraints)

print("\nTabelas registradas no metadata:")
print(metadata_obj.tables)

print("\nTabelas ordenadas:")
for table in metadata_obj.sorted_tables:
    print(table)