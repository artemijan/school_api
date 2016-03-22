# Initial
```shell
virtualenv env
source env/bin/activate
pip install Flask
pip install SQLAlchemy
```
# Information about Models in API
- we are using [sqlAlchemy](http://www.sqlalchemy.org/), so you need to check this docs first
- each implemented Model class should have "\__plural__" property (is needed for "jsonify", array representation) 
and should extend class Serializable form common.utils module:
```py
class User(Base, Serializable):
    __tablename__ = 'users'
    __plural__ = 'users'
    __write_only__ = () # tuple, fields that wouldn't be in serialized data, because they are write only ("password_hash" for example)
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %>' % self.name
```