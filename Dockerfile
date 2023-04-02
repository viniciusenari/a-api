# Use the official Python image as base
FROM python:3.11.2-slim


# Install Poetry and configure virtual environments
RUN pip install poetry==1.4.1
RUN poetry config virtualenvs.create false

# Copy the project files
COPY pyproject.toml poetry.lock ./
COPY app ./app/
COPY main.py ./

# Install project dependencies
RUN poetry install --no-dev --no-root

# Expose port 80
EXPOSE 80

# Start the ASGI server (Uvicorn)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
