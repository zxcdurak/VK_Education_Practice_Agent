# Используем официальный образ Python 3.10.11 slim (меньше размер, быстрее загрузка)
# Образ основан на Debian. Если нужен Alpine, замените на python:3.10.11-alpine
FROM python:3.10.11-slim

WORKDIR /src

# Копируем файл зависимостей (requirements.txt) в рабочую директорию
# Копируем сначала только requirements.txt, чтобы использовать кэш Docker слоев
# если зависимости не изменились, пересборка будет быстрее
COPY requirements.txt .

# Устанавливаем зависимости из requirements.txt
# --no-cache-dir: Не сохраняет пакеты в кэш, уменьшает размер образа
# --upgrade: Обновляет пакеты, если они уже установлены (часто используется для pip)
# pip install --upgrade pip: Убедимся, что у нас последняя версия pip
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем остальной код приложения в рабочую директорию
COPY . .

# Порт
EXPOSE 8000 

CMD ["python", "main.py"]