"""
Application Flask - Bibliothèque CRUD + Chatbot AI (Groq)
"""
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import requests
from models import Livre, LivreRepository, DatabaseConfig

app = Flask(__name__)
CORS(app)

# ─── Configuration ────────────────────────────────────────────
DB_CONFIG = DatabaseConfig(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", ""),
    database=os.getenv("DB_NAME", "bibliotheque")
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "VOTRE_CLE_GROQ_ICI")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL   = "llama-3.3-70b-versatile"

repo = LivreRepository(DB_CONFIG)


# ══════════════════════════════════════════════════════════════
#  PAGE PRINCIPALE
# ══════════════════════════════════════════════════════════════

@app.route("/")
def index():
    return render_template("index.html")


# ══════════════════════════════════════════════════════════════
#  CRUD LIVRES
# ══════════════════════════════════════════════════════════════

@app.route("/api/livres", methods=["GET"])
def lister_livres():
    page      = int(request.args.get("page", 1))
    par_page  = int(request.args.get("par_page", 10))
    recherche = request.args.get("recherche", "")
    categorie = request.args.get("categorie", "")
    resultat  = repo.lire_tous(page, par_page, recherche, categorie)
    return jsonify({"success": True, "data": resultat})


@app.route("/api/livres/<int:id_livre>", methods=["GET"])
def obtenir_livre(id_livre):
    livre = repo.lire_par_id(id_livre)
    if not livre:
        return jsonify({"success": False, "message": "Livre non trouvé"}), 404
    return jsonify({"success": True, "data": livre})


@app.route("/api/livres", methods=["POST"])
def creer_livre():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Données invalides"}), 400

    for champ in ["titre", "auteur", "categorie", "annee_publication", "quantite_disponible"]:
        if champ not in data:
            return jsonify({"success": False, "message": f"Champ manquant : {champ}"}), 400

    try:
        livre = Livre(
            titre=data["titre"],
            auteur=data["auteur"],
            categorie=data["categorie"],
            annee_publication=int(data["annee_publication"]),
            quantite_disponible=int(data["quantite_disponible"]),
            statut=data.get("statut", "disponible")
        )
        livre_cree = repo.creer(livre)
        return jsonify({"success": True, "data": livre_cree.to_dict(), "message": "Livre créé avec succès"}), 201
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/livres/<int:id_livre>", methods=["PUT"])
def modifier_livre(id_livre):
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Données invalides"}), 400
    if not repo.lire_par_id(id_livre):
        return jsonify({"success": False, "message": "Livre non trouvé"}), 404

    succes = repo.mettre_a_jour(id_livre, data)
    if succes:
        return jsonify({"success": True, "data": repo.lire_par_id(id_livre), "message": "Livre mis à jour"})
    return jsonify({"success": False, "message": "Aucune modification effectuée"}), 400


@app.route("/api/livres/<int:id_livre>", methods=["DELETE"])
def supprimer_livre(id_livre):
    if not repo.lire_par_id(id_livre):
        return jsonify({"success": False, "message": "Livre non trouvé"}), 404
    succes = repo.supprimer(id_livre)
    if succes:
        return jsonify({"success": True, "message": "Livre supprimé avec succès"})
    return jsonify({"success": False, "message": "Erreur lors de la suppression"}), 500


@app.route("/api/statistiques", methods=["GET"])
def statistiques():
    stats = repo.statistiques()
    return jsonify({"success": True, "data": stats})


# ══════════════════════════════════════════════════════════════
#  CHATBOT AI — ROUTE SÉPARÉE  /api/chatbot
# ══════════════════════════════════════════════════════════════

def construire_contexte_bibliotheque() -> str:
    """Contexte compact pour rester dans les limites de tokens Groq."""
    livres = repo.lire_tous_pour_chatbot()
    if not livres:
        return "La bibliothèque est vide."

    lignes = ["CATALOGUE (id|titre|auteur|categorie|annee|quantite|statut):"]
    for l in livres:
        lignes.append(
            f"{l['id_livre']}|{l['titre']}|{l['auteur']}|"
            f"{l['categorie']}|{l['annee_publication']}|"
            f"{l['quantite_disponible']}ex|{l['statut']}"
        )

    stats = repo.statistiques()
    lignes.append(
        f"\nSTATS: {stats['total_livres']} livres | "
        f"{stats['disponibles']} disponibles | "
        f"{stats['empruntes']} empruntés | "
        f"{stats['reserves']} réservés"
    )
    return "\n".join(lignes)


@app.route("/api/chatbot", methods=["POST"])
def chatbot():
    """
    POST /api/chatbot
    Body: { "message": "...", "historique": [...] }
    """
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"success": False, "message": "Message manquant"}), 400

    message_utilisateur = data["message"].strip()
    historique = data.get("historique", [])

    if not message_utilisateur:
        return jsonify({"success": False, "message": "Message vide"}), 400

    contexte = construire_contexte_bibliotheque()

    system_prompt = (
        "Tu es BiblioBot, assistant de bibliothèque. Réponds en français, de façon concise.\n"
        "Tu peux aider à : trouver des livres, vérifier la disponibilité, recommander des livres.\n"
        "Pour créer/modifier/supprimer un livre, dis à l'utilisateur d'utiliser l'interface CRUD.\n\n"
        + contexte
    )

    messages = [{"role": "system", "content": system_prompt}]

    # Historique limité aux 4 derniers échanges pour éviter dépassement de tokens
    for msg in historique[-4:]:
        if msg.get("role") in ["user", "assistant"] and msg.get("content"):
            messages.append({"role": msg["role"], "content": msg["content"]})

    messages.append({"role": "user", "content": message_utilisateur})

    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": GROQ_MODEL,
            "messages": messages,
            "max_tokens": 512,
            "temperature": 0.7,
            "stream": False
        }

        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=30)

        # Log détaillé si erreur 400
        if response.status_code == 400:
            err = response.json()
            print(">>> Groq 400 error:", err)
            msg_err = err.get("error", {}).get("message", "Bad Request")
            return jsonify({"success": False, "message": f"Groq 400: {msg_err}"}), 400

        if response.status_code == 401:
            return jsonify({"success": False, "message": "Clé API Groq invalide. Vérifiez GROQ_API_KEY."}), 401

        response.raise_for_status()
        result = response.json()
        reponse_bot = result["choices"][0]["message"]["content"]

        return jsonify({
            "success": True,
            "reponse": reponse_bot,
            "model": GROQ_MODEL,
            "tokens_utilises": result.get("usage", {})
        })

    except requests.exceptions.Timeout:
        return jsonify({"success": False, "message": "Timeout : Groq ne répond pas"}), 504
    except requests.exceptions.HTTPError as e:
        return jsonify({"success": False, "message": f"Erreur Groq API: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"success": False, "message": f"Erreur interne: {str(e)}"}), 500


# ══════════════════════════════════════════════════════════════
#  INITIALISATION
# ══════════════════════════════════════════════════════════════

@app.route("/api/init", methods=["POST"])
def initialiser():
    """POST /api/init — Initialise la BDD et insère les 50 livres."""
    from seed import inserer_donnees_initiales
    try:
        repo.initialiser_base()
        inserer_donnees_initiales(repo)
        return jsonify({"success": True, "message": "Base de données initialisée avec 50 livres !"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


if __name__ == "__main__":
    try:
        repo.initialiser_base()
        print("✅ Connexion MySQL établie")
    except Exception as e:
        print(f"⚠️  Erreur MySQL : {e}")

    app.run(debug=True, host="0.0.0.0", port=5000)