import mysql.connector
from mysql.connector import Error
import os

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "bibliotheque"),
    "charset": "utf8mb4",
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def init_db():
    """Initialise la base de données et la table livres."""
    cfg = dict(DB_CONFIG)
    cfg.pop("database")
    conn = mysql.connector.connect(**cfg)
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    cursor.execute(f"USE {DB_CONFIG['database']}")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS livres (
            id_livre      INT AUTO_INCREMENT PRIMARY KEY,
            titre         VARCHAR(255)  NOT NULL,
            auteur        VARCHAR(255)  NOT NULL,
            categorie     VARCHAR(100)  NOT NULL,
            annee_publication INT,
            quantite_disponible INT DEFAULT 1,
            statut        ENUM('disponible','emprunté','réservé') DEFAULT 'disponible'
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    conn.commit()
    cursor.close()
    conn.close()
