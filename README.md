# 🚀 LinkedIn AutoApply Bot

Ce projet automatise le processus de candidature aux offres d'emploi sur LinkedIn via Selenium et génère automatiquement les réponses aux questions des formulaires grâce à GPT (via g4f).

## ✅ Fonctionnalités

- Connexion automatique à LinkedIn.
- Recherche d’offres et candidatures automatiques via **"Candidature simplifiée"**.
- Détection des questions posées dans le formulaire.
- Génération de réponses personnalisées avec GPT (basées sur votre CV).
- Remplissage automatique des champs de texte.
- Navigation automatique entre les pages de résultats.

## ⚙️ Prérequis

- Python 3.10+
- Google Chrome avec le bon ChromeDriver installé.
- Un fichier **`cv.txt`** contenant votre CV pour la génération de réponses.
- Compte LinkedIn valide.

## 🛠 Installation

```bash
git clone https://github.com/RatovosonPascal/Linkedin_Apply_Selenium_python/tree/dev
cd linkedin-autoapply-bot
pip install -r requirements.txt
