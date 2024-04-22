# Використовуємо офіційний контейнер Python 3.11
FROM python:3.11

# Встановлюємо poetry
RUN pip install --no-cache-dir poetry

# Переміщуємо файли проекту в робочу директорію /code
WORKDIR /code
COPY . /code

# Виконуємо команди встановлення залежностей з використанням poetry
RUN poetry install

# Запускаємо додаток за допомогою Uvicorn
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
