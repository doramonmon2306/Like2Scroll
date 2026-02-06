# Like2Scroll

Like2Scroll is a simple computer-vision project that enables **scrolling control using hand gestures**.  
It uses a hand-landmark detection model together with Python to recognize gestures and translate them into scrolling actions.

---

## Features
- Real-time **hand landmark detection**
- Gesture-based **scroll interaction**
- Lightweight Python implementation
- Demo video included in the repository

---

## Project Structure
```
Like2Scroll/
│
├── main.py                # Main application script
├── hand_landmarker.task   # Hand landmark detection model
├── demo.gif               # Demo video
└── README.md
```
The repository mainly consists of a Python script, a trained hand-landmarker model file, and a sample demo video.

---

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/doramonmon2306/Like2Scroll.git
cd Like2Scroll
```

> Adjust dependencies if your local setup differs.

### 2. Run the project
```bash
python main.py
```

---

## Demo

Below is a short demonstration of the gesture-based scrolling system:

![](https://github.com/doramonmon2306/Like2Scroll/blob/main/demo.gif)

If the video does not load on GitHub preview, download and play **`demo.gif`** locally from the repository.  
The demo file is included directly in the project files.

---

## How It Works
1. The webcam captures real-time hand movement.
2. A hand-landmark model detects finger positions.
3. Specific gestures are mapped to scrolling actions.
4. The system sends scroll commands to the operating system.

---

# Like2Scroll(Version Française)

Like2Scroll est un projet simple de vision par ordinateur qui permet le **contrôle du défilement à l'aide de gestes de la main**.  
Il utilise un modèle de détection de points de repère de la main avec Python pour reconnaître les gestes et les traduire en actions de défilement.

---

## Fonctionnalités
- Détection en temps réel des **points de repère de la main**
- Interaction de **défilement basée sur les gestes**
- Implémentation légère en Python
- Vidéo de démonstration incluse dans le dépôt

---

## Structure du Projet
```
Like2Scroll/
│
├── main.py                # Script principal de l'application
├── hand_landmarker.task   # Modèle de détection des points de la main
├── demo.gif               # Vidéo de démonstration
└── README.md
```
Le dépôt contient principalement un script Python, un fichier de modèle de détection de la main entraîné et une vidéo de démonstration.

---

## Pour Commencer

### 1. Cloner le dépôt
```bash
git clone https://github.com/doramonmon2306/Like2Scroll.git
cd Like2Scroll
```

> Ajustez les dépendances si votre configuration locale diffère.

### 2. Exécuter le projet
```bash
python main.py
```

---

## Démonstration

Voici une courte démonstration du système de défilement basé sur les gestes :

![](https://github.com/doramonmon2306/Like2Scroll/blob/main/demo.gif)

Si la vidéo ne se charge pas dans l'aperçu GitHub, téléchargez et lisez **`demo.gif`** localement depuis le dépôt.  
Le fichier de démonstration est inclus directement dans les fichiers du projet.

---

## Comment Ça Marche
1. La webcam capture les mouvements de la main en temps réel.
2. Un modèle de points de repère de la main détecte les positions des doigts.
3. Des gestes spécifiques sont associés à des actions de défilement.
4. Le système envoie des commandes de défilement au système d'exploitation.

---

