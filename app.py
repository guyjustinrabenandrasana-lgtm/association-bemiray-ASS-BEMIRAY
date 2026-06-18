from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect("membres.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    conn = get_db_connection()
    membres = conn.execute("SELECT * FROM membres").fetchall()
    conn.close()
    return render_template("index.html", membres=membres)


# 🔥 NOUVELLE ROUTE
@app.route("/ajouter", methods=["GET", "POST"])
def ajouter():
    if request.method == "POST":
        nom = request.form["nom"]
        prenom = request.form["prenom"]
        email = request.form["email"]
        tel = request.form["tel"]

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO membres (nom, prenom, email, tel) VALUES (?, ?, ?, ?)",
            (nom, prenom, email, tel)
        )
        conn.commit()
        conn.close()

        return redirect("/")  # retour à la page principale

    return render_template("ajouter.html")


@app.route("/supprimer/<int:id>")
def supprimer(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM membres WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect("/")
@app.route("/modifier/<int:id>", methods=["GET", "POST"])
def modifier(id):
    conn = get_db_connection()

    # 🔥 Si on envoie le formulaire
    if request.method == "POST":
        nom = request.form["nom"]
        prenom = request.form["prenom"]
        email = request.form["email"]
        tel = request.form["tel"]

        conn.execute(
            "UPDATE membres SET nom = ?, prenom = ?, email = ?, tel=? WHERE id = ?",
            (nom, prenom, email, tel, id)
        )
        conn.commit()
        conn.close()

        return redirect("/")

    # 🔥 Sinon → afficher le formulaire avec les données existantes
    membre = conn.execute(
        "SELECT * FROM membres WHERE id = ?",
        (id,)
    ).fetchone()

    conn.close()

    return render_template("modifier.html", membre=membre)

app.run(debug=True)