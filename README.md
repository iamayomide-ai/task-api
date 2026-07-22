# Task API — Python + Git + Docker Practice Project

A tiny task-manager REST API (built with FastAPI) meant as a hands-on
sandbox for practicing three skills at once: writing Python, managing
the code with Git, and running it in Docker.

## Project layout

```
task-api/
├── app/
│   ├── __init__.py
│   └── main.py          # the API
├── tests/
│   └── test_main.py     # pytest tests
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .gitignore
└── README.md
```

## 1. Run it locally with plain Python (no Docker yet)

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt

uvicorn app.main:app --reload
```

Visit http://localhost:8000/docs for the interactive Swagger UI.

Run the tests:
```bash
pytest
```

## 2. Turn it into a Git repo

```bash
git init
git add .
git commit -m "Initial commit: task API skeleton"
```

Good next reps for Git practice:
- Create a `feature/add-priority-field` branch, add a `priority` field
  to `TaskIn`, commit, then merge it back to `main`.
- Make a bad commit on purpose, then practice `git reset --soft HEAD~1`
  or `git revert`.
- Push to GitHub/GitLab and open a pull request against your own `main`.
- Try `git log --oneline --graph` to visualize your branch history.

## 3. Run it with Docker

Build and run manually:
```bash
docker build -t task-api .
docker run -p 8000:8000 task-api
```

Or with Compose (rebuilds + mounts your code for live-reload):
```bash
docker compose up --build
```

Check the container's health status:
```bash
docker ps          # look at the STATUS column
docker inspect --format='{{json .State.Health}}' <container_id>
```

Good next reps for Docker practice:
- Add a second service to `docker-compose.yml` — e.g. swap the
  in-memory `tasks` dict for a real Postgres database and connect
  to it from `app/main.py`.
- Multi-stage build: split the Dockerfile into a "builder" stage and
  a slim "runtime" stage to shrink the final image.
- Push your image to Docker Hub: `docker tag task-api yourname/task-api`
  then `docker push yourname/task-api`.
- Add a `.dockerignore` file so `.venv/`, `.git/`, etc. never get
  copied into the image context.

## 4. Combine both: a simple CI mindset

Once comfortable, try wiring up a GitHub Actions workflow
(`.github/workflows/ci.yml`) that on every push:
1. Installs dependencies
2. Runs `pytest`
3. Builds the Docker image

That gives you one project touching Python, Git branching/PRs, Docker,
and (optionally) CI — a solid all-in-one practice loop.
