from flask import Flask, request, jsonify
import pikepdf
import base64
from io import BytesIO

app = Flask(__name__)

@app.route('/', methods=['GET'])
def health():
    return jsonify({"status": "PDF Unlocker is running"})

@app.route('/unlock', methods=['POST'])
def unlock():
    try:
        data = request.get_json()
        if not data or 'pdf_base64' not in data:
            return jsonify({"error": "Missing pdf_base64"}), 400

        pdf_bytes = base64.b64decode(data['pdf_base64'])

        with pikepdf.open(BytesIO(pdf_bytes), suppress_warnings=True) as pdf:
            output = BytesIO()
            pdf.save(output)

        return jsonify({
            "pdf_base64": base64.b64encode(output.getvalue()).decode('utf-8'),
            "success": True
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
