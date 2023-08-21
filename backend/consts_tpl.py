from get_docker_secret import get_docker_secret

db_username = get_docker_secret('MIAMI_POSTGRES_USER') or 'op://Private/Miami Local Postgres Root Password/username'
db_password = get_docker_secret('MIAMI_POSTGRES_PASSWORD') or 'op://Private/Miami Local Postgres Root Password/password'
db_name = get_docker_secret('MIAMI_POSTGRES_DB') or 'op://Private/Miami Local Postgres Root Password/database'
flask_api_secret = get_docker_secret('MIAMI_FLASK_SECRET') or 'op://Private/Miami Flask Secret Key Local/password'
