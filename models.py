"""
Modèle Livre avec CRUD complet en POO - MySQL
Correction : nouvelle connexion à chaque requête pour éviter "Lost connection"
"""
import mysql.connector
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Livre:
    titre: str
    auteur: str
    categorie: str
    annee_publication: int
    quantite_disponible: int
    statut: str = "disponible"
    id_livre: Optional[int] = None

    def to_dict(self):
        return {
            "id_livre": self.id_livre,
            "titre": self.titre,
            "auteur": self.auteur,
            "categorie": self.categorie,
            "annee_publication": self.annee_publication,
            "quantite_disponible": self.quantite_disponible,
            "statut": self.statut,
        }


class DatabaseConfig:
    def __init__(self, host="localhost", user="root", password="", database="bibliotheque"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database


class LivreRepository:
    """
    Chaque méthode ouvre et ferme sa propre connexion pour éviter
    l'erreur 2013: Lost connection to MySQL server.
    """

    def __init__(self, config: DatabaseConfig):
        self.config = config

    def _get_connection(self):
        """Crée une nouvelle connexion MySQL fraîche à chaque appel."""
        return mysql.connector.connect(
            host=self.config.host,
            user=self.config.user,
            password=self.config.password,
            database=self.config.database,
            connection_timeout=30,
            autocommit=False
        )

    def initialiser_base(self):
        conn = mysql.connector.connect(
            host=self.config.host,
            user=self.config.user,
            password=self.config.password,
            connection_timeout=30
        )
        try:
            cursor = conn.cursor()
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS {self.config.database} "
                f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
            conn.database = self.config.database
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS livres (
                    id_livre INT AUTO_INCREMENT PRIMARY KEY,
                    titre VARCHAR(255) NOT NULL,
                    auteur VARCHAR(255) NOT NULL,
                    categorie ENUM('Roman','Science','Histoire','Informatique','Philosophie','Art','Économie','Biographie') NOT NULL,
                    annee_publication INT NOT NULL,
                    quantite_disponible INT DEFAULT 1,
                    statut ENUM('disponible','emprunté','réservé') DEFAULT 'disponible',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            conn.commit()
            cursor.close()
        finally:
            conn.close()

    def creer(self, livre: Livre) -> Livre:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO livres (titre, auteur, categorie, annee_publication, quantite_disponible, statut)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (livre.titre, livre.auteur, livre.categorie,
                  livre.annee_publication, livre.quantite_disponible, livre.statut))
            conn.commit()
            livre.id_livre = cursor.lastrowid
            cursor.close()
            return livre
        finally:
            conn.close()

    def lire_tous(self, page=1, par_page=10, recherche="", categorie="") -> dict:
        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            conditions, params = [], []
            if recherche:
                conditions.append("(titre LIKE %s OR auteur LIKE %s)")
                params.extend([f"%{recherche}%", f"%{recherche}%"])
            if categorie:
                conditions.append("categorie = %s")
                params.append(categorie)
            where = "WHERE " + " AND ".join(conditions) if conditions else ""

            cursor.execute(f"SELECT COUNT(*) as total FROM livres {where}", params)
            total = cursor.fetchone()["total"]
            offset = (page - 1) * par_page
            cursor.execute(
                f"SELECT * FROM livres {where} ORDER BY id_livre DESC LIMIT %s OFFSET %s",
                params + [par_page, offset]
            )
            livres = cursor.fetchall()
            cursor.close()
            return {
                "livres": livres, "total": total, "page": page,
                "par_page": par_page,
                "total_pages": (total + par_page - 1) // par_page
            }
        finally:
            conn.close()

    def lire_par_id(self, id_livre: int) -> Optional[dict]:
        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM livres WHERE id_livre = %s", (id_livre,))
            livre = cursor.fetchone()
            cursor.close()
            return livre
        finally:
            conn.close()

    def lire_tous_pour_chatbot(self) -> List[dict]:
        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM livres ORDER BY titre")
            livres = cursor.fetchall()
            cursor.close()
            return livres
        finally:
            conn.close()

    def statistiques(self) -> dict:
        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT
                    COUNT(*) as total_livres,
                    SUM(quantite_disponible) as total_exemplaires,
                    COUNT(CASE WHEN statut='disponible' THEN 1 END) as disponibles,
                    COUNT(CASE WHEN statut='emprunté' THEN 1 END) as empruntes,
                    COUNT(CASE WHEN statut='réservé' THEN 1 END) as reserves
                FROM livres
            """)
            stats = cursor.fetchone()
            cursor.execute(
                "SELECT categorie, COUNT(*) as nb FROM livres GROUP BY categorie ORDER BY nb DESC"
            )
            stats["par_categorie"] = cursor.fetchall()
            cursor.close()
            return stats
        finally:
            conn.close()

    def mettre_a_jour(self, id_livre: int, donnees: dict) -> bool:
        champs_autorises = {"titre", "auteur", "categorie", "annee_publication", "quantite_disponible", "statut"}
        donnees_filtrees = {k: v for k, v in donnees.items() if k in champs_autorises}
        if not donnees_filtrees:
            return False
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            set_clause = ", ".join([f"{k} = %s" for k in donnees_filtrees])
            valeurs = list(donnees_filtrees.values()) + [id_livre]
            cursor.execute(f"UPDATE livres SET {set_clause} WHERE id_livre = %s", valeurs)
            conn.commit()
            modifie = cursor.rowcount > 0
            cursor.close()
            return modifie
        finally:
            conn.close()

    def supprimer(self, id_livre: int) -> bool:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM livres WHERE id_livre = %s", (id_livre,))
            conn.commit()
            supprime = cursor.rowcount > 0
            cursor.close()
            return supprime
        finally:
            conn.close()

    def fermer(self):
        pass  # Plus de connexion persistante à fermer