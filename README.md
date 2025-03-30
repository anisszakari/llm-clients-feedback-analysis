# 📢 Feedback Analysis Project

Ce projet analyse les **feedbacks clients** en utilisant un **LLM** (Large Language Model) pour détecter le **sentiment**. 
Si un feedback est négatif, un **email** est envoyé automatiquement à l'équipe support et au client.  
Le tout est déployé sur **Google Cloud Run** avec **Terraform** et une pipeline **CI/CD via GitHub Actions**.

---

## 📌 **Architecture du projet**
### 🏗️ **Les services :**
1. **`llm_analysis_service`** 🧠  
   - Analyse le feedback avec un **LLM** (ex: OpenAI GPT-4).
   - Stocke les résultats dans **BigQuery**.
   - Publie l’analyse sur **Pub/Sub**.

2. **`negative_feedback_handler`** 🚨  
   - Récupère les feedbacks négatifs via **Pub/Sub**.
   - Envoie un **email** au support + au client concerné.

---

## 🛠️ **Installation & Déploiement**

### **1️⃣ Prérequis**  
- **Google Cloud SDK** installé ([lien](https://cloud.google.com/sdk/docs/install))
- Un projet **GCP** avec :
  - **Cloud Run** activé
  - **BigQuery** et **Pub/Sub** configurés
  - **IAM Service Account** avec les permissions nécessaires  
- **Docker** installé  
- **Terraform** installé  

### **2️⃣ Cloner le repo**  
```sh
git clone https://github.com/anisszakari/llm-clients-feedback-analysis.git
cd llm-clients-feedback-analysis
```

### **3️⃣ Configurer les variables GCP**  
Dans **GitHub Secrets** (si CI/CD) ou en local dans `.env` :  

| Variable | Description |
|----------|-------------|
| `GCP_PROJECT_ID` | ID du projet GCP |
| `OPENAI_API_KEY` | Clé API OpenAI |
| `SENDGRID_API_KEY` | Clé API SendGrid |

---

## 🚀 **Déploiement Automatique (CI/CD)**  

### **1️⃣ Configuration GitHub Actions**  
Dans **GitHub > Repo > Settings > Secrets** ➝ Ajouter :  
- `GCP_PROJECT_ID`  
- `GCP_SA_KEY` (clé JSON du Service Account)  
- `OPENAI_API_KEY`  
- `SENDGRID_API_KEY`  

### **2️⃣ Push sur `main`**  
À chaque push sur `main`, GitHub Actions :  
✅ **Construit et push l’image Docker sur GCR**  
✅ **Déploie sur Cloud Run**  

---

## 🚀 **Déploiement Manuel** (Sans CI/CD)  

### **1️⃣ Déploiement avec Terraform**  
```sh
terraform init
terraform apply
```

### **2️⃣ Déploiement avec un script**  
```sh
chmod +x deploy.sh
./deploy.sh
```

---

## 📡 **Exemple d'utilisation API**

### **Analyser un feedback**  
```sh
curl -X POST "https://llm-analysis-service-url/analyze_feedback/"      -H "Content-Type: application/json"      -d '{"feedback_id": "123", "feedback_text": "Votre service est horrible !"}'
```
📌 **Réponse attendue :**  
```json
{
  "feedback_id": "123",
  "sentiment": "Négatif"
}
```

---

