# Build stage
FROM python:3.11-slim-bullseye as builder

RUN apt-get -qq update && apt-get -qq install python3-dev gcc libc-dev -y
RUN pip install pipenv

WORKDIR /app
COPY ./src/Pipfile* ./
RUN pipenv lock && pipenv requirements > requirements.txt
RUN pip install --no-cache-dir -r requirements.txt --prefix=/install

#
# ----------------------------------------------------------------------
#

# Final stage
FROM python:3.11-slim-bullseye

# Don't generate .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turn off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Copy only the installed packages from the build stage
WORKDIR /app
COPY --from=builder /install /usr/local
COPY --chown=nobody:nogroup ./src .

# Force install certifi
RUN pip install certifi

USER nobody
EXPOSE 8080

CMD ["streamlit", "run", "index.py"]
