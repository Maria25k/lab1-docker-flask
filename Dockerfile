cat > Dockerfile << 'EOF'
FROM python:3.11-slim AS builder
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt
FROM python:3.11-slim AS runner
WORKDIR /usr/src/app
COPY --from=builder /install /usr/local
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
EOF