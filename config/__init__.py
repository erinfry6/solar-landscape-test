import os

if os.getenv('ENV') == 'production':
    from .production_config import DATABASE
else:
    from .development_config import DATABASE