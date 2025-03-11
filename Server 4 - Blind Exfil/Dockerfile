# Use Python 3.10 base image
FROM python:3-alpine3.10

# Set the working directory inside the container
# Copy the application files to the container
WORKDIR /app
COPY app.py flag.py requirements.txt /app/
COPY templates/ /app/templates/

# Ensure the /flag directory exists and copy flag.txt
RUN mkdir -p /flag
COPY flag.txt /flag/flag.txt
#RUN chmod 700 /flag && \
#    chmod 400 /flag/flag.txt && \
#    chown root:root /flag /flag/flag.txt

# Install required system dependencies for lxml
RUN apk add --no-cache libxml2-dev libxslt-dev gcc musl-dev python3-dev
RUN pip install supervisor

# Upgrade pip and install Python dependencies
#RUN pip install --upgrade pip && \
RUN pip install --no-cache-dir -r requirements.txt

# Create a configuration file for supervisord
RUN mkdir -p /etc/supervisor/conf.d
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Switch to non-root user
RUN adduser -D secureuser
USER secureuser

# Expose the application port
EXPOSE 5000

# Start both Flask apps using supervisord
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]