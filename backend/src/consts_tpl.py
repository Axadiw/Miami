from get_docker_secret import get_docker_secret

db_username = get_docker_secret('MIAMI_POSTGRES_USER') or 'op://Private/Miami Local Postgres Root Password/username'
db_password = get_docker_secret('MIAMI_POSTGRES_PASSWORD') or 'op://Private/Miami Local Postgres Root Password/password'
db_name = get_docker_secret('MIAMI_POSTGRES_DB') or 'op://Private/Miami Local Postgres Root Password/database'

flask_api_secret = '1cc52f74f7f3bbbca31c1e1368230358'
