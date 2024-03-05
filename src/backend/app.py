from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('virtual_machine_prices.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/offers', methods=['GET'])
def get_offers():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 100))
    offset = (page - 1) * limit
    conn = get_db_connection()
    offers = conn.execute('SELECT * FROM offers LIMIT ? OFFSET ?', (limit, offset)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in offers])

if __name__ == '__main__':
    app.run(debug=True)
