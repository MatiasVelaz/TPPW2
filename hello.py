from flask import Flask, request, jsonify
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

#  Datos en memoria
productos = [
    {"id": 1, "nombre": "Manzana", "precio": 100},
    {"id": 2, "nombre": "Banana", "precio": 80},
    {"id": 3, "nombre": "Tomate", "precio": 120},
    {"id": 4, "nombre": "Lechuga", "precio": 90}
]

carrito = []

# productos
@app.route('/api/productos', methods=['GET'])
def get_productos():
    """
    Obtener lista de productos
    ---
    responses:
      200:
        description: Lista de productos disponibles
    """
    return jsonify(productos)

#  POST agregar al carrito
@app.route('/api/carrito', methods=['POST'])
def agregar_carrito():
    """
    Agregar producto al carrito
    ---
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - producto_id
          properties:
            producto_id:
              type: integer
    responses:
      200:
        description: Producto agregado al carrito
      404:
        description: Producto no encontrado
    """
    data = request.get_json()
    producto_id = data.get('producto_id')

    producto = next((p for p in productos if p['id'] == producto_id), None)

    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404

    carrito.append(producto)
    return jsonify({"mensaje": "Producto agregado", "carrito": carrito})

# eliminar del carrito
@app.route('/api/carrito', methods=['DELETE'])
def eliminar_carrito():
    """
    Eliminar producto del carrito
    ---
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - producto_id
          properties:
            producto_id:
              type: integer
    responses:
      200:
        description: Producto eliminado
      404:
        description: Producto no encontrado en carrito
    """
    data = request.get_json()
    producto_id = data.get('producto_id')

    for item in carrito:
        if item['id'] == producto_id:
            carrito.remove(item)
            return jsonify({"mensaje": "Producto eliminado", "carrito": carrito})

    return jsonify({"error": "Producto no está en el carrito"}), 404

# total
@app.route('/api/total', methods=['GET'])
def calcular_total():
    """
    Calcular total del carrito
    ---
    responses:
      200:
        description: Total de la compra
    """
    total = sum(p['precio'] for p in carrito)
    return jsonify({"total": total})

# pa que arranque la maldita maquina
if __name__ == '__main__':
    app.run(debug=True)