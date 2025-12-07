
---

### **1. Copy the template**

* Copy the whole folder to a new project folder:

```bash
cp -r fastapi-base-template my-new-project
cd my-new-project
```

---

### **2. Rename project references**

* This is mostly for Docker image names, container names, and readability:

  * **Docker Compose**:

    * `docker-compose.yml`: change service names (`api`, `db`, `redis`) to include your project name.
    * Example: `fastapi-base-template-api` → `mynewproject-api`
  * **Dockerfile**:

    * You can optionally tag the image differently: `fastapi-base-template-api` → `mynewproject-api`
  * **App folder**:

    * Keep `app/` as-is. No need to rename for FastAPI.
  * **Alembic**:

    * `alembic.ini` URL can remain the same; DB name might change (optional).

---

### **3. Update `.env`**

* Create a new `.env` file for the new project.
* Update ports, DB name, Redis ports, secrets if needed.
* Example:

```
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
POSTGRES_DB=mynewproject_db
POSTGRES_PORT=5432

REDIS_HOST=redis
REDIS_PORT=6379

API_PORT=8080
```

---

### **4. Update `requirements.txt` if needed**

* Add project-specific packages:

  * `ollama`, `huggingface_hub`, `langchain`, etc.
* Keep existing stable packages (FastAPI, Alembic, SQLAlchemy, Redis, Pydantic, etc.).

---

### **5. Setup database**

* Start containers:

```bash
docker compose up -d
```

* If DB name changed, update `alembic.ini` with new DB URL.

* Run initial migrations:

```bash
docker compose exec api alembic revision --autogenerate -m "initial migration"
docker compose exec api alembic upgrade head
```

---

### **6. Add your project-specific models**

* Put in `app/models/`
* Add schemas in `app/schemas/`
* Add routes in `app/api/v1/routes/`
* You can reuse the `CRUDRepository` for any new model.

---

### **7. Add project-specific services**

* `app/services/`: For Ollama/HuggingFace/LangChain logic
* Keep these modular and call from routes or background tasks.

---

### **8. Update main.py**

* Include new routers for your models:

```python
from app.api.v1.routes import user, mymodel_router

app.include_router(user.router)
app.include_router(mymodel_router.router)
```

---

### **9. Test CRUD and services**

* Use Postman or curl to test endpoints.
* Make sure DB and Redis connections work.
* Apply migrations as needed for new models.

---

### **10. Optional enhancements**

* JWT auth / roles (`app/core/security.py`)
* Async support if required
* Background tasks for AI processing

---

✅ **Summary**:
For each new project, just **copy template → rename ports/names → update `.env` → add models/routes/services → run migrations → start building your AI features**.

---

