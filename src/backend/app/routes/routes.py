from flask import request
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
        
@api.route('/offer-types')
class OfferTypesResource(Resource):
    @api.doc('get_offer_types')
    def get(self):
        offer_types = Offer.query.with_entities(Offer.offer_type).distinct().all()
        if offer_types:
            return {'offer_types': [offer_type[0] for offer_type in offer_types]}
        
        return {'message': 'No SKUs provided'}, 400
    
@api.route('/pricing-types')
class OfferTypesResource(Resource):
    @api.doc('get_offer_types')
    def get(self):
        offer_types = Offer.query.with_entities(Offer.pricing_type).distinct().all()
        if offer_types:
            return {'pricing_types': [pricing_type[0] for pricing_type in offer_types]}
        
        return {'message': 'No SKUs provided'}, 400