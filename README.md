# Mission 1 — Taggage automatique des plaintes consommateurs

Projet d'exploration data-science / IA : comparaison d'approches **ML classique** et **LLM** pour automatiser le taggage de plaintes consommateurs (données CFPB), afin de router chaque plainte vers la bonne équipe de support.

---

## Prérequis

- **Python 3.13** (voir `.python-version`)
- **[uv](https://docs.astral.sh/uv/)** comme gestionnaire de paquets (pas de `pip` / `venv` manuel)

### Installer uv

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Alternative via pip
pip install uv
```

Vérification :

```bash
uv --version
```

---

## Installation du projet

### Cloner le dépôt et synchroniser l'environnement

```bash
git clone <url-du-repo>
cd <nom-du-repo>

# Crée .venv et installe les dépendances exactes depuis uv.lock
uv sync
```

`uv sync` lit `pyproject.toml` + `uv.lock`, crée `.venv/` et installe tout (dépendances du projet **et** groupe `dev`).

### Initialiser un projet à partir de zéro (référence)

Si vous recréez la structure vous-même :

```bash
uv init --package mission-1     # crée pyproject.toml avec structure src/
uv add pandas numpy matplotlib seaborn scikit-learn sentence-transformers
uv add --dev ipykernel nbclient nbconvert nbformat
uv lock                         # génère/met à jour uv.lock
uv sync                         # installe selon le lockfile
```

### Commandes uv utiles

| Commande                | Rôle                                                            |
| ----------------------- | --------------------------------------------------------------- |
| `uv sync`               | Installe les dépendances selon `uv.lock`                        |
| `uv lock`               | Régénère le lockfile après modification de `pyproject.toml`     |
| `uv add <paquet>`       | Ajoute une dépendance (met à jour `pyproject.toml` + `uv.lock`) |
| `uv add --dev <paquet>` | Ajoute une dépendance de dev                                    |
| `uv remove <paquet>`    | Supprime une dépendance                                         |
| `uv run <cmd>`          | Exécute une commande dans l'environnement du projet             |

> **Important :** toujours passer par `uv add` pour ajouter une dépendance, ne pas utiliser `pip install`.

---

## Notebook d'exploration

Le travail d'exploration se trouve dans `src/app/exploration.ipynb` (annotations en français), exécuté avec le kernel **`zenassist`** (« Python (ZenAssist) »).

Si le kernel n'existe pas encore, l'enregistrer contre le venv :

```bash
uv run python -m ipykernel install --name zenassist --display-name "Python (ZenAssist)"
```

---

## Lancer l'API FastAPI

```bash
uv run fastapi dev
```

### Modèle ML : téléchargement automatique

À **chaque démarrage** de l'API, le fichier du modèle entraîné est **récupéré depuis une release** du dépôt (GitHub Releases) et chargé en mémoire. Conséquences :

- Une **connexion internet** est nécessaire au démarrage.
- Le modèle utilisé correspond à la release référencée dans la configuration de l'API : pour changer de version de modèle, publier une nouvelle release et mettre à jour la référence correspondante.
- Le démarrage peut être plus long selon la taille du fichier modèle.

---

> `.venv/` et les artefacts de build sont gitignorés : ne pas les committer.
