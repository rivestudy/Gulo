from flask import Blueprint, request, jsonify, render_template, current_app

ppg_bp = Blueprint("ppg", __name__)

@ppg_bp.route("/")
def index():
    return render_template("index.html")

@ppg_bp.route("/ppg", methods=["GET"])
def get_ppg():
    cursor = current_app.config['DB'].cursor()
    cursor.execute("SELECT id, ppg, nir, waktu FROM ppg_data ORDER BY waktu DESC")
    result = cursor.fetchall()
    cursor.close()

    data = [{
        "id": row[0],
        "ppg": row[1],
        "nir": row[2],
        "waktu": row[3].strftime('%Y-%m-%d %H:%M:%S')
    } for row in result]

    return jsonify(data)

@ppg_bp.route("/ppg/<int:id>", methods=["PATCH"])
def update_ppg(id):
    data = request.get_json()
    ppg, nir = data.get("ppg"), data.get("nir")
    cursor = current_app.config['DB'].cursor()
    cursor.execute("UPDATE ppg_data SET ppg = %s, nir = %s WHERE id = %s", (ppg, nir, id))
    current_app.config['DB'].commit()
    cursor.close()

    return jsonify({"message": f"Data dengan ID {id} berhasil diupdate!"})

@ppg_bp.route("/ppg/init", methods=["POST"])
def init_ppg():
    cursor = current_app.config['DB'].cursor()
    cursor.execute("INSERT INTO ppg_data (ppg, nir) VALUES (0, 0)")
    current_app.config['DB'].commit()
    cursor.close()

    return jsonify({"message": "Baris awal berhasil dibuat!"})
