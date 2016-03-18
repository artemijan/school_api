# Information about Models in app
## Structure:
- we are using [sqlAlchemy](http://www.sqlalchemy.org/), so you need to check this docs first
- each implemented Model class should have "__plural__" property (is needed for "jsonify", array representation)