# Build stage
FROM python:3.9-alpine3.14 as builder

RUN apk update && apk add python3-dev gcc libc-dev
RUN pip install pipenv streamlit

WORKDIR /app
COPY ./src/Pipfile* ./
RUN pipenv lock && pipenv requirements > requirements.txt
RUN pip install --no-cache-dir -r requirements.txt --prefix=/install

# Final stage
FROM python:3.9-alpine3.14

WORKDIR /app

# Copy only the installed packages from the build stage
COPY --from=builder /install /usr/local

COPY --chown=nobody:nogroup ./src .

USER nobody

EXPOSE 8080

CMD ["streamlit", "run", "index.py"]
