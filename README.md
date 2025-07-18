
---

## 🔐 Managing Sensitive Configs with `.env`

Instead of hardcoding sensitive configurations like `FERNET_KEY` in `docker-compose.yml`, we use a `.env` file.

### ✅ Step 1: Install requirements.txt and generate FERNET_KEY

Run inside terminal: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
to get key.

### ✅ Step 2: Create a `.env` file

Create a file named `.env` at the root of your project with the following content and add key:

```env
# .env

FERNET_KEY=
AIRFLOW_IMAGE_NAME=apache/airflow:3.0.0
# Optional: add other environment variables if needed
