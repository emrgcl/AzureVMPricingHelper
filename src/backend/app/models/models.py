from ..database import db

class Offer(db.Model):
    __tablename__ = 'offers'
    id = db.Column(db.INTEGER, primary_key=True)
    sku = db.Column(db.TEXT)
    pricing_type = db.Column(db.TEXT)
    offer_sku = db.Column(db.TEXT)
    offer_type = db.Column(db.TEXT)
    region = db.Column(db.TEXT)
    price = db.Column(db.REAL)

    def __repr__(self):
        return f"<Offer {self.sku}>"
