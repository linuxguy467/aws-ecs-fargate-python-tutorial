import logging

# Define loggers and handlers
error_logger = logging.getLogger("gunicorn.error")
access_logger = logging.getLogger("gunicorn.access")

# Configure error logger
error_logger.handlers.clear()
error_logger.addHandler(logging.FileHandler("gunicorn_error.log"))
error_logger.setLevel(logging.ERROR)

# Configure access logger
access_logger.handlers.clear()
access_logger.addHandler(logging.FileHandler("gunicorn_access.log"))
access_logger.setLevel(logging.INFO)

# Configure Gunicorn settings
bind = "0.0.0.0:8081"  # Specify the IP address and port to bind to
workers = 4  # Number of worker processes

# Use this option to preload your application before workers are forked
# This can help with performance and resource usage for larger applications
preload_app = True

# Set the maximum number of requests a worker will process before restarting
max_requests = 1000

# Set the maximum number of requests a worker will process before graceful shutdown
max_requests_jitter = 50

# Configure the loggers used by Gunicorn
accesslog = "-"  # Send access logs to stdout
errorlog = "-"  # Send error logs to stdout
