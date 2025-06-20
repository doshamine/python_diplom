FROM python:3.12

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

RUN chmod +x /start.sh
ENTRYPOINT ["/start.sh"]
