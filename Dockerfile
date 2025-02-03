FROM python:3.11-alpine3.20
LABEL maintainer="erfanscode"

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy files
COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app

# Working directory
WORKDIR /app
EXPOSE 8000

# Install dependencies
RUN pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user


# Set the environment variable PATH
ENV PATH="/py/bin:$PATH"

# Switch to 'django-user' to avoid running as root for security reasons
USER django-user