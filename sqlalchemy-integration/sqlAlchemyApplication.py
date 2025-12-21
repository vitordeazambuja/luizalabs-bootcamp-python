from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, func, inspect, select
from sqlalchemy.orm import declarative_base, relationship, Session

Base = declarative_base()

class User(Base):
    __tablename__ = "user_account"

    # Atributos
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

    address = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f'User(id={self.id}, name={self.name}, fullname={self.fullname})'

class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email_address = Column(String(30), nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    user = relationship(
        "User", back_populates="address"
    )

    def __repr__(self):
        return f'Address(id={self.id}, email={self.email_address})'
    
# Conexão com o banco de dados
engine = create_engine("sqlite://")

# Criando as classes como tabelas no banco de dados
Base.metadata.create_all(engine)

# Investiga o banco de dados
inspetor_engine = inspect(engine)

print(inspetor_engine.has_table("user_account"))
print(inspetor_engine.get_table_names())
print(inspetor_engine.default_schema_name)


with Session(engine) as session:
    juliana = User(
        name='juliana',
        fullname='Juliana Mascarenhas',
        address=[Address(email_address='julianam@email.com')]
    )

    sandy = User(
        name='sandy',
        fullname='Sandy Cardoso',
        address=[Address(email_address='sandy@email.com'),
                 Address(email_address='sandy@email.br')]
    )

    patrick = User(
        name='patrick',
        fullname='Patrick Cardoso'
    )

    # Enviando para o BD (persistência de dados)
    session.add_all([juliana, sandy, patrick])

    session.commit()

stmt = select(User).where(User.name.in_(['juliana', 'sandy']))
print('\nRecuperando usuários a partir de condição de filtragem')
for user in session.scalars(stmt):
    print(user)

stmt_address = select(Address).where(Address.user_id.in_([2]))
print('\nRecuperando os endereços de email de Sandy')
for address in session.scalars(stmt_address):
    print(address)

stmt_order = select(User).order_by(User.fullname.desc())
print('\nRecuperando info de maneira ordenada')
for result in session.scalars(stmt_order):
    print(result)

stmt_join = select(User.fullname, Address.email_address).join_from(Address, User)
print('\n')
for result in session.scalars(stmt_join):
    print(result)

connection = engine.connect()
results = connection.execute(stmt_join).fetchall()
print("\nExecutando a statement a partir da connection")
for result in results:
    print(result)

stmt_count = select(func.count('*')).select_from(User)
print('\nTotal de instâncias em User')
for result in session.scalars(stmt_count):
    print(result)