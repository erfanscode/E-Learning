FROM python:3.11-alpine3.20
LABEL maintainer="erfanscode"

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Working directory
WORKDIR /education

# Copy files
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY . .

ARG DEV=false

# Set the environment variable PATH
ENV PATH="/py/bin:$PATH"

# Install dependencies
RUN python -m venv /py && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp

# Create and configure user
RUN adduser \
    --disabled-password \
    --no-create-home \
    django-user && \
    chown -R django-user:django-user /education

# Expose port for application
EXPOSE 8000

# Switch to 'django-user' to avoid running as root for security reasons
USER django-user