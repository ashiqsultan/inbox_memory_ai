
## Using yoyo-migrations cli

Make sure to run the migrations using the docker container.

1. Login to the fastapi container using the following command:

```
 docker exec -it <fastapi-container-id> /bin/bash
```

2. List the migrations using the following command:
   This will list all the migrations in the /migrations directory.

```
yoyo list --database postgresql://postgres:postgres@postgres:5432/inbox_memory_db .
```

3. Apply the migrations using the following command: This will ask you to confirm before applying the migrations one by one. You need to answer with y or n for each migration.

```
yoyo apply --database postgresql://postgres:postgres@postgres:5432/inbox_memory_db .
```

4. To Rollback the migrations, you can use the following command:

```
yoyo rollback --database postgresql://postgres:postgres@postgres:5432/inbox_memory_db .
```

Make sure each migration files have a unique name and a respective rollback file.
The rollback file should have the same name as the migration file but with a `.rollback.sql` suffix.
Example:

```
0009_add_user_table.sql
0009_add_user_table.rollback.sql
```
