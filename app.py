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
            return jsonify({"error": "Missing pdf_base64 in request body"}), 400

        # Decode base64 PDF
        pdf_bytes = base64.b64decode(data['pdf_base64'])

        # Open with pikepdf — strips owner-password restrictions without needing the password
        with pikepdf.open(BytesIO(pdf_bytes), suppress_warnings=True) as pdf:
            output = BytesIO()
            pdf.save(output)
            unlocked_bytes = output.getvalue()

        # Return unlocked PDF as base64
        return jsonify({
            "pdf_base64": base64.b64encode(unlocked_bytes).decode('utf-8'),
            "success": True
        })

    except pikepdf.PasswordError:
        return jsonify({"error": "PDF is locked with a user password and cannot be opened"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
