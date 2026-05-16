# 📚 Bibliothèque CRUD + Chatbot AI (Groq)

Application Python/Flask de gestion de bibliothèque avec CRUD complet en POO,
base MySQL, 50 livres de démo, et un chatbot IA propulsé par Groq.

## 🏗 Structure du projet

```
bibliotheque/
├── app.py          # Application Flask + routes API + chatbot
├── models.py       # Classes POO : Livre + LivreRepository (CRUD)
├── seed.py         # Jeu de 50 livres pour initialiser la BDD
├── requirements.txt
├── .env.example    # Variables d'environnement à copier
└── templates/
    └── index.html  # Interface web complète
```

## ⚙️ Installation

### 1. Prérequis
- Python 3.9+
- MySQL 8.0+
- Compte Groq gratuit (https://console.groq.com)

### 2. Cloner et installer les dépendances
```bash
cd bibliotheque
pip install -r requirements.txt
```

### 3. Configurer les variables d'environnement
```bash
cp .env.example .env
# Éditez .env avec vos credentials MySQL et clé Groq
```

### 4. Démarrer l'application
```bash
python app.py
```

L'application est disponible sur : **http://localhost:5000**

### 5. Initialiser les 50 livres
```bash
curl -X POST http://localhost:5000/api/init
```
Ou via le bouton dans l'interface.

---

## 🔗 Routes API

### CRUD Livres

| Méthode | Route               | Description              |
|---------|---------------------|--------------------------|
| GET     | /api/livres         | Liste paginée + filtres  |
| GET     | /api/livres/:id     | Détail d'un livre        |
| POST    | /api/livres         | Créer un livre           |
| PUT     | /api/livres/:id     | Modifier un livre        |
| DELETE  | /api/livres/:id     | Supprimer un livre       |
| GET     | /api/statistiques   | Stats globales           |

#### Paramètres GET /api/livres
```
?page=1&par_page=10&recherche=Hugo&categorie=Roman
```

#### Body POST/PUT
```json
{
  "titre": "Les Misérables",
  "auteur": "Victor Hugo",
  "categorie": "Roman",
  "annee_publication": 1862,
  "quantite_disponible": 3,
  "statut": "disponible"
}
```

### Chatbot AI

| Méthode | Route         | Description                          |
|---------|---------------|--------------------------------------|
| POST    | /api/chatbot  | Envoyer un message au chatbot Groq   |

#### Body
```json
{
  "message": "Quels livres de science sont disponibles ?",
  "historique": [
    { "role": "user", "content": "..." },
    { "role": "assistant", "content": "..." }
  ]
}
```

---

## 🤖 Obtenir une clé Groq gratuite

1. Allez sur https://console.groq.com
2. Créez un compte (gratuit)
3. **API Keys** → **Create API Key**
4. Copiez la clé dans `.env` : `GROQ_API_KEY=gsk_...`

Le modèle utilisé est **llama-3.3-70b-versatile** (gratuit, très rapide).

---

## 📐 Architecture POO

```python
# Livre : dataclass représentant un livre
@dataclass
class Livre:
    titre: str
    auteur: str
    categorie: str
    annee_publication: int
    quantite_disponible: int
    statut: str = "disponible"
    id_livre: Optional[int] = None

# LivreRepository : toutes les opérations CRUD
class LivreRepository:
    def creer(self, livre: Livre) -> Livre        # CREATE
    def lire_tous(self, page, ...) -> dict        # READ (liste)
    def lire_par_id(self, id) -> dict             # READ (1 livre)
    def mettre_a_jour(self, id, donnees) -> bool  # UPDATE
    def supprimer(self, id) -> bool               # DELETE
```

---

## 📊 Catégories disponibles
`Roman` · `Science` · `Histoire` · `Informatique` · `Philosophie` · `Art` · `Économie` · `Biographie`

## 📋 Statuts disponibles
`disponible` · `emprunté` · `réservé`
