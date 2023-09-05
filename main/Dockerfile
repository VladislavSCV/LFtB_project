FROM python


# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN pip install -r requirements.txt

# Copy the source code into the container.
COPY requirements.txt .

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD ['python', 'manage.py', 'runserver']