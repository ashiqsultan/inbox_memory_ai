## Start Prod or dev
```
doker compose up --build -d
```
### See logs
```
docker logs -f <container name or id>
```

## Setup ngrok for development

```
docker run --rm -it --net=host \
  -e NGROK_AUTHTOKEN=<secret> \
  ngrok/ngrok:latest \
  http 8002
```

## Using yoyo-migrations CLI

Make sure to run the migrations using the Docker container.

### 1. Login to the running FastAPI container

```
docker exec -it <fastapi-container-id> /bin/bash
```

### 2. List migrations

Navigate to the migrations folder and list all available migrations:

```
cd migrations
yoyo list --database postgresql://postgres:postgres@postgres:5432/inbox_memory_db .
```

This will list all the migrations in the `/migrations` directory.

### 3. Apply migrations

Apply the migrations using the following command. You will be prompted to confirm each migration individually:

```
yoyo apply --database postgresql://postgres:postgres@postgres:5432/inbox_memory_db .
```

### 4. Rollback migrations

To rollback migrations, use:

```
yoyo rollback --database postgresql://postgres:postgres@postgres:5432/inbox_memory_db .
```

### Migration file naming convention

Each migration file must have a unique name with a corresponding rollback file. The rollback file should have the same name as the migration file but with a `.rollback.sql` suffix.

Example:
```
001_user_table.sql
001_user_table.rollback.sql
```
