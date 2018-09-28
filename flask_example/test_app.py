import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy, DefaultMeta, declarative_base, Model

MyModel = declarative_base(
    cls=Model,
    name='MyModel',
    metaclass=DefaultMeta
)


class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


app_a = Flask('app_a')
app_a.config.from_object(Config)
db_a = SQLAlchemy(app_a, model_class=MyModel)

app_b = Flask('app_b')
app_b.config.from_object(Config)
db_b = SQLAlchemy(app_b, model_class=MyModel)

print(db_a.session)


class A(db_a.Model):
    __tablename__ = 'a'
    id = db_a.Column(db_a.Integer, primary_key=True, autoincrement=True)
    content = db_a.Column(db_a.Text, nullable=False)


class B(db_b.Model):
    __tablename__ = 'b'
    id = db_b.Column(db_b.Integer, primary_key=True, autoincrement=True)
    content = db_b.Column(db_b.Text, nullable=False)


@app_a.route('/a')
def a():
    #a_s = A.query.all()
    a_s = db_a.session.query(A).all()
    return str([a.content for a in a_s])


@app_b.route('/b')
def b():
    #bs = B.query.all()
    bs = db_b.session.query(B).all()
    return str([b.content for b in bs])


print(
    A.query.session == B.query.session,
    db_a.session.query(A) == db_b.session.query(B)
)

db_a.session.remove()
db_b.session.remove()

s1 = A.query.session
s2 = B.query.session
s3 = db_a.session()
s4 = db_b.session()
print(s1 == s2, s1 == s3, s1 == s4, s2 == s3, s2 == s4, s3 == s4)


class TestA(unittest.TestCase):
    app = app_a
    db = db_a

    def setUp(self):
        self.app.testing = True
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db.create_all()

        a_s = [A(content='a%d' % i)for i in range(10)]
        self.db.session.add_all(a_s)
        self.db.session.commit()
        self.db.session.remove()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()
        self.db.engine.dispose()
        self.app_context.pop()

    def test1(self):
        rsp = self.client.get('/a')

    def test2(self):
        rsp = self.client.get('/a')


class TestB(unittest.TestCase):
    app = app_b
    db = db_b

    def setUp(self):
        self.app.testing = True
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db.create_all()

        bs = [B(content='b%d' % i)for i in range(10)]
        self.db.session.add_all(bs)
        self.db.session.commit()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()
        self.db.engine.dispose()
        self.app_context.pop()

    def test1(self):
        rsp = self.client.get('/b')

    def test2(self):
        rsp = self.client.get('/b')
