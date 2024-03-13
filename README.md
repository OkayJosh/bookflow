# Bookflow

Bookflow is a simple Django web application utilizing Docker and PostgreSQL.

## Prerequisites

Before you start, ensure you have the following installed:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

1. Clone this repository:

    ```bash
    git clone https://github.com/OkayJosh/bookflow.git
    cd bookflow
    ```

2. Copy a `.env.tp` file in the project root and create a new file as `.env` with the content:
    ```bash
    #!/bin/bash

    # Check if .env.tp exists
    if [ ! -f .env.tp ]; then
        echo "Error: .env.tp file not found. Please make sure .env.tp exists in the project root."
        exit 1
    fi

    # Copy .env.tp to .env
    cp .env.tp .env

    echo "Successfully copied .env.tp to .env"
    ```
3. Build and run the Docker containers:

    ```bash
    sudo chmod -R +rX .
   ```
   
   ```bash
    docker compose build
    docker compose up -d
    ```

    then run this seeding:

    ```bash
    docker compose run web
    ```

4. Open your web browser and navigate to [http://0.0.0.0:8000](http://localhost:8000) to access the Django app.
5.  Use password ```password``` and username ```student1```

## Notes

- The Django app runs on port 8000. You can customize the port in the `docker-compose.yml` file.

- The PostgreSQL database is configured with the credentials specified in the `.env` file.

- Adjust the Django settings and configurations in the `Bookflow/settings.py` file as needed.

## Contributing

Feel free to contribute by opening issues or creating pull requests. Contributions are welcome!

