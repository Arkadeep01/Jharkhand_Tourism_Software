FROM python:3.11.8-alpine3.18
WORKDIR /app
RUN apk add --no-cache gcc musl-dev libffi-dev
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
