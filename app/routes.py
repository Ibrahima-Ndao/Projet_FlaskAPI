from flask import Blueprint, request, jsonify
from app import db
from app.models import ElectronicProduct
from app.schemas import ElectronicProductSchema
from flask_jwt_extended import jwt_required

api_bp = Blueprint('api_bp', __name__)

product_schema = ElectronicProductSchema()
products_schema = ElectronicProductSchema(many=True)

@api_bp.route('/products', methods=['GET'])
def get_products():
    products = ElectronicProduct.query.all()
    return products_schema.jsonify(products)

@api_bp.route('/product/<int:id>', methods=['GET'])
@jwt_required()
def get_product(id):
    product = ElectronicProduct.query.get_or_404(id)
    return product_schema.jsonify(product)

@api_bp.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    data = request.get_json()
    new_product = ElectronicProduct(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        brand=data['brand'],
        model_number=data['model_number'],
        category=data['category'],
        stock=data.get('stock', 0)
    )
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product)

@api_bp.route('/product/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    product = ElectronicProduct.query.get_or_404(id)
    data = request.get_json()
    product.name = data['name']
    product.description = data['description']
    product.price = data['price']
    product.brand = data['brand']
    product.model_number = data['model_number']
    product.category = data['category']
    product.stock = data.get('stock', product.stock)
    db.session.commit()
    return product_schema.jsonify(product)

@api_bp.route('/product/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    product = ElectronicProduct.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"})
