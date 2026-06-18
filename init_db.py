import sqlite3

# Connexion (crée le fichier si il n'existe pas)
conn = sqlite3.connect("membres.db")

# Création de la table
conn.execute("""
CREATE TABLE membres (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT,
    prenom TEXT,
    email TEXT,
    tel INTEGER
)
""")

# Sauvegarde
conn.commit()

# Fermeture
conn.close()

print("Base de données créée !")