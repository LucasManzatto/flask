FROM python:3.7-alpine

WORKDIR /src

COPY . .

RUN apk add --no-cache gcc musl-dev linux-headers

RUN pip install -r requirements.txt

CMD flask run --host=0.0.0.0