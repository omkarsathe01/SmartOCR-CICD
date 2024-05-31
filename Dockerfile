FROM python:3.10.9

WORKDIR /work/Blue-Bricks-OCR

COPY . .

RUN chmod 777 -R /work/Blue-Bricks-OCR

RUN pip install gunicorn

RUN pip install --no-cache-dir -r requirement.txt

RUN apt update \
  && apt -y install libgl1-mesa-glx \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

EXPOSE 5000

CMD ["sh", "start.sh"]
