FROM mcr.microsoft.com/playwright/python:v1.58.0-noble

WORKDIR /automation

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

RUN playwright install chromium --with-deps

COPY . .

CMD ["pytest", "--browser", "chromium", "--headless"]