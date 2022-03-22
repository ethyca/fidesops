# Quickstart
The [Fidesops repository](https://github.com/ethyca/fidesops) includes a built-in docker compose configuration for quickly experimenting with a working demo environment. 

For a more detailed guide on Fidesops, [the tutorial](tutorial/index.md) provides an in-depth introduction, and a [full installation guide](deployment.md) is available for production deployments.

## Requirements

* [Docker 12+](https://docs.docker.com/desktop/#download-and-install)
* Python 3.7+
* Make (`brew install make` via Homebrew on Mac, Make for Windows, or your preferred installation)


## Running Fidesops locally 

Ensure nothing is running on ports `8080`, `5432`, or `6379` prior to these steps.

1. Clone the [Fidesops repository](https://github.com/ethyca/fidesops).
   
2. Run `make server` from the root of the Fidesops project directory. The provided `docker-compose.yml` will create the necessary databases and spin up the server.
   
3. Visit `http://0.0.0.0:8080/health` in your browser, where a response of `{ "healthy": true }` will confirm a successful deployment.
   
### Example Docker-compose file

```yaml title="<code>docker-compose.yml</code>"
services:
  fidesops:
    image: ethyca/fidesops
    container_name: fidesops
    depends_on:
      - db
      - redis
    expose:
      - 8080
    healthcheck:
      test: ["CMD", "curl", "-f", "http://0.0.0.0:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 1s
    ports:
      - "8080:8080"
    volumes:
      - type: bind
        source: ./
        target: /fidesops #Update this to the path of your project directory
        read_only: False

  db:
    image: postgres:12
    volumes:
      - app-db-data:/var/lib/postgresql/data/pgdata
    environment:
      - PGDATA=/var/lib/postgresql/data/pgdata
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=216f4b49bea5da4f84f05288258471852c3e325cd336821097e1e65ff92b528a
      - POSTGRES_DB=app

    expose:
      - 5432
    ports:
      - "0.0.0.0:5432:5432"
    deploy:
      placement:
        constraints:
          - node.labels.fidesops.app-db-data == true

  redis:
    image: "redis:6.2.5-alpine"
    command: redis-server --requirepass testpassword
    environment:
      - REDIS_PASSWORD=testpassword
    expose:
      - 6379
    ports:
      - "0.0.0.0:6379:6379"

volumes:
  app-db-data:
```

1. To replicate the demo environment in your own project, create a `docker-compose.yml` file like the example in your application's root directory.
   
2. Ensure Docker is running, and run `docker compose up` (or `docker compose up -d` to run the docker-compose file in the background) from the project's root directory. This will pull the latest Fidesops Docker image, create the sample databases, and start the server.

3. Visit `http://0.0.0.0:8080/health` in your browser, where a response of `{ "healthy": true }` will confirm a successful deployment.

## Next Steps
You now have a functional test installation of Fidesops running! From here, use the available [How-To Guides](guides/oauth.md) to view examples of authenticating, connecting to databases, configuring policies, and more. 