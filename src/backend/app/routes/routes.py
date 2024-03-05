from flask_restx import Namespace, Resource, fields
from ..models.models import Offer
from ..database import db

api = Namespace('offers', description='Offers related operations')

offer_model = api.model('Offer', {
    'sku': fields.String(required=True, description='The SKU'),
    'pricing_type': fields.String(required=True, description='The pricing type'),
    'offer_sku': fields.String(required=True, description='The offer SKU'),
    'offer_type': fields.String(required=True, description='The offer type'),
    'region': fields.String(required=True, description='The region'),
    'price': fields.Float(required=True, description='The price'),
})

@api.route('/<string:sku>')
@api.param('sku', 'The SKU identifier')
@api.response(404, 'Offer not found')
class OfferResource(Resource):
    @api.doc('get_offer')
    @api.marshal_with(offer_model)
    def get(self, sku):
        offer = Offer.query.filter_by(sku=sku).all()
        if offer:
            return offer
        api.abort(404)
