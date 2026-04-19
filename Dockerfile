FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && \
    pip install streamlit pandas plotly openai python-dotenv

EXPOSE 10000

CMD ["sh", "-c", "streamlit run scripts/app.py --server.address=0.0.0.0 --server.port=${PORT:-10000}"]