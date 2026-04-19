FROM mcr.microsoft.com/playwright:v1.59.1-noble

WORKDIR /automation

COPY requirements.txt .

RUN pip install -r --no-cache-dir requirements.txt

RUN playwright install chromium --with-deps

COPY . .

CMD ["pytest", "--browser", "chromium", "--headless"]