from . import db

class Rssfeed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    source = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable = False ,default="New")

    def __repr__(self):
        return f"<Rssfeed '{self.title}'>"