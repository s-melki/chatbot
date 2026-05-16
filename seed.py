"""
Jeu de données : 50 livres variés pour initialiser la bibliothèque.
"""
from models import Livre

LIVRES_INITIAUX = [
    # ─── Romans ───────────────────────────────────────────────
    Livre("Les Misérables", "Victor Hugo", "Roman", 1862, 4, "disponible"),
    Livre("Le Comte de Monte-Cristo", "Alexandre Dumas", "Roman", 1844, 3, "disponible"),
    Livre("Madame Bovary", "Gustave Flaubert", "Roman", 1857, 2, "emprunté"),
    Livre("L'Étranger", "Albert Camus", "Roman", 1942, 5, "disponible"),
    Livre("Le Petit Prince", "Antoine de Saint-Exupéry", "Roman", 1943, 6, "disponible"),
    Livre("Germinal", "Émile Zola", "Roman", 1885, 2, "réservé"),
    Livre("Notre-Dame de Paris", "Victor Hugo", "Roman", 1831, 3, "disponible"),
    Livre("Voyage au bout de la nuit", "Louis-Ferdinand Céline", "Roman", 1932, 2, "disponible"),
    Livre("La Peste", "Albert Camus", "Roman", 1947, 4, "emprunté"),
    Livre("Bel-Ami", "Guy de Maupassant", "Roman", 1885, 2, "disponible"),
    Livre("1984", "George Orwell", "Roman", 1949, 5, "disponible"),
    Livre("Le Meilleur des Mondes", "Aldous Huxley", "Roman", 1932, 3, "disponible"),
    Livre("Dune", "Frank Herbert", "Roman", 1965, 4, "réservé"),
    Livre("Harry Potter et la Chambre des Secrets", "J.K. Rowling", "Roman", 1998, 5, "disponible"),
    Livre("Le Seigneur des Anneaux", "J.R.R. Tolkien", "Roman", 1954, 3, "emprunté"),

    # ─── Science ──────────────────────────────────────────────
    Livre("Une brève histoire du temps", "Stephen Hawking", "Science", 1988, 4, "disponible"),
    Livre("L'Univers élégant", "Brian Greene", "Science", 1999, 2, "disponible"),
    Livre("Le Gène égoïste", "Richard Dawkins", "Science", 1976, 3, "disponible"),
    Livre("Cosmos", "Carl Sagan", "Science", 1980, 3, "réservé"),
    Livre("La Relativité", "Albert Einstein", "Science", 1916, 2, "disponible"),
    Livre("Origines de la vie", "François Jacob", "Science", 1970, 1, "disponible"),
    Livre("Sapiens : Une brève histoire de l'humanité", "Yuval Noah Harari", "Science", 2011, 5, "emprunté"),
    Livre("La Structure des révolutions scientifiques", "Thomas Kuhn", "Science", 1962, 2, "disponible"),

    # ─── Histoire ─────────────────────────────────────────────
    Livre("Histoire de la Révolution française", "Jules Michelet", "Histoire", 1847, 2, "disponible"),
    Livre("La Seconde Guerre mondiale", "Winston Churchill", "Histoire", 1948, 3, "disponible"),
    Livre("L'Art de la guerre", "Sun Tzu", "Histoire", -500, 4, "disponible"),
    Livre("Le Prince", "Niccolò Machiavel", "Histoire", 1532, 3, "disponible"),
    Livre("Civilisation et Capitalisme", "Fernand Braudel", "Histoire", 1967, 1, "réservé"),
    Livre("Les Croisades vues par les Arabes", "Amine Maalouf", "Histoire", 1983, 3, "disponible"),
    Livre("De la démocratie en Amérique", "Alexis de Tocqueville", "Histoire", 1835, 2, "emprunté"),
    Livre("Histoire de l'Islam", "Marshall Hodgson", "Histoire", 1974, 2, "disponible"),

    # ─── Informatique ─────────────────────────────────────────
    Livre("Introduction aux algorithmes", "Thomas H. Cormen", "Informatique", 1990, 3, "disponible"),
    Livre("Le Langage C", "Kernighan & Ritchie", "Informatique", 1978, 2, "disponible"),
    Livre("Clean Code", "Robert C. Martin", "Informatique", 2008, 4, "emprunté"),
    Livre("Design Patterns", "Gang of Four", "Informatique", 1994, 3, "disponible"),
    Livre("The Pragmatic Programmer", "Hunt & Thomas", "Informatique", 1999, 2, "disponible"),
    Livre("Apprendre Python", "Mark Lutz", "Informatique", 2013, 5, "réservé"),
    Livre("Deep Learning", "Ian Goodfellow", "Informatique", 2016, 3, "disponible"),
    Livre("Structure and Interpretation of Computer Programs", "Abelson & Sussman", "Informatique", 1985, 2, "disponible"),

    # ─── Philosophie ──────────────────────────────────────────
    Livre("La République", "Platon", "Philosophie", -380, 3, "disponible"),
    Livre("Éthique à Nicomaque", "Aristote", "Philosophie", -350, 2, "disponible"),
    Livre("Méditations", "René Descartes", "Philosophie", 1641, 3, "disponible"),
    Livre("Critique de la raison pure", "Emmanuel Kant", "Philosophie", 1781, 2, "emprunté"),
    Livre("Ainsi parlait Zarathoustra", "Friedrich Nietzsche", "Philosophie", 1883, 4, "disponible"),

    # ─── Biographie ───────────────────────────────────────────
    Livre("Mémoires de guerre", "Charles de Gaulle", "Biographie", 1954, 2, "disponible"),
    Livre("Long Walk to Freedom", "Nelson Mandela", "Biographie", 1994, 3, "disponible"),
    Livre("Steve Jobs", "Walter Isaacson", "Biographie", 2011, 4, "emprunté"),
    Livre("Elon Musk", "Ashlee Vance", "Biographie", 2015, 3, "disponible"),
    Livre("Journal d'Anne Frank", "Anne Frank", "Biographie", 1947, 5, "disponible"),
    Livre("Les Confessions", "Jean-Jacques Rousseau", "Biographie", 1782, 2, "réservé"),
]


def inserer_donnees_initiales(repository):
    """Insère les 50 livres dans la base de données."""
    print(f"Insertion de {len(LIVRES_INITIAUX)} livres...")
    for livre in LIVRES_INITIAUX:
        repository.creer(livre)
    print("✅ Jeu de données inséré avec succès !")
