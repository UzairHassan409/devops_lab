import os
from pathlib import Path
import textwrap
from flask import Flask
import os

# main.py
# GitHub Copilot
# Utility to scaffold a repo with Dockerfile and GitHub Actions CI/CD workflow.
# Run this script from your project root to create files and print the git commands to run.


ROOT = Path.cwd()

files = {
    "app.py": textwrap.dedent("""\

        app = Flask(__name__)

        @app.route("/")
        def hello():
            return "Hello from CI/CD demo"

        if __name__ == "__main__":
            port = int(os.environ.get("PORT", 8080))
            app.run(host="0.0.0.0", port=port)
        """),
    "requirements.txt": "flask\n",
    "Dockerfile": textwrap.dedent("""\
        FROM python:3.11-slim

        WORKDIR /app

        COPY requirements.txt .
        RUN pip install --no-cache-dir -r requirements.txt

        COPY . .

        ENV PORT=8080
        EXPOSE 8080

        CMD [ "python", "app.py" ]
        """),
    ".dockerignore": textwrap.dedent("""\
        __pycache__
        .git
        .venv
        *.pyc
        """),
    ".gitignore": textwrap.dedent("""\
        __pycache__/
        *.pyc
        .venv/
        .env
        """),
    "README.md": textwrap.dedent("""\
        # CI/CD Demo

        Simple Flask app to demonstrate GitHub Actions building and pushing a Docker image.

        - Build locally: `docker build -t <yourname>/cicd-demo:latest .`
        - Run locally: `docker run -p 8080:8080 <yourname>/cicd-demo:latest`
        """),
    ".github/workflows/ci-cd.yml": textwrap.dedent("""\
        name: CI/CD

        on:
          push:
            branches: [ main ]

        jobs:
          build-and-push:
            runs-on: ubuntu-latest

            steps:
              - uses: actions/checkout@v4

              - name: Set up QEMU
                uses: docker/setup-qemu-action@v2

              - name: Set up Docker Buildx
                uses: docker/setup-buildx-action@v3

              - name: Login to GitHub Container Registry
                uses: docker/login-action@v2
                with:
                  registry: ghcr.io
                  username: ${{ github.actor }}
                  password: ${{ secrets.GITHUB_TOKEN }}

              - name: Build and push Docker image
                uses: docker/build-push-action@v4
                with:
                  context: .
                  push: true
                  tags: ghcr.io/${{ github.repository }}/cicd-demo:latest
        """),
}

def write_file(path: Path, content: str):
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        print(f"skip: {path} (already exists)")
    else:
        path.write_text(content, encoding="utf-8")
        print(f"created: {path}")

def main():
    for rel, content in files.items():
        write_file(ROOT / rel, content)

    instructions = textwrap.dedent("""\
        NEXT STEPS (run these in your terminal)

        1) Initialize git and make the first commit:
           git init
           git add .
           git commit -m "Initial commit"

        2) Create a repository on GitHub, then add remote and push:
           git branch -M main
           git remote add origin https://github.com/USERNAME/REPO.git
           git push -u origin main

        3) After pushing to main, GitHub Actions (CI/CD) will run the workflow:
           - It builds a Docker image and pushes to GitHub Container Registry (ghcr.io).
           - To push to Docker Hub instead, update the workflow to login to docker.io and set DOCKER_USERNAME/DOCKER_PASSWORD as secrets.

        Useful git commands:
           git status
           git pull origin main
           git push

        Local Docker test:
           docker build -t <yourname>/cicd-demo:latest .
           docker run -p 8080:8080 <yourname>/cicd-demo:latest

        SHORT CI/CD EXPLANATION:
        CI/CD automates building, testing, and deploying code on each push. This reduces manual steps,
        catches integration issues early, and speeds up delivery by ensuring a repeatable, auditable pipeline.
        """)
    print("\n" + instructions)

if __name__ == "__main__":
    main()