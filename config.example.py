"""
    Apply relevant changes to this file, and rename as config.py
"""
import os

# Define if the application is running in debug mode
# Expected value = Boolean
DEBUG = True

# Manual configuration for testing environment
# Expected value = Boolean
TEST_ENV = False

# Define port to run the application on
# Expected value = Integer
PORT = 8080

#======================================================================
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
#======================================================================

# Specify default encoding for the application
DEFAULT_ENCODING = 'utf-8'

DATABASE_LOC = '/path/to/db'

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "18b49521e895ace6ae5277a87a2ac0f5"

# Secret key for signing cookies
SECRET_KEY = "18b49521e895ace6ae5277a87a2ac0f5"
