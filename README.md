# Trab1 Web

## Set up the project

Install uv, if you don't have it already.
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install the dependencies:

```bash
uv sync
```

Apply the migrations:
```bash
python manage.py migrate
```

Create a superuser (if you want to access the admin panel):
```bash
python manage.py createsuperuser
```

## Run the dev server

```bash
python manage.py runserver
```

## Contributing

Install the pre-commit hooks:

```bash
uv run pre-commit install
```
