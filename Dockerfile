FROM python:3.12-slim

WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y build-essential

# Копируем requirements
COPY requirements.txt .

# Ставим зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# CMD ["bash"]
