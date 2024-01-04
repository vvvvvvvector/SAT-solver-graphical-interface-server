An open source application built using [FastAPI](https://fastapi.tiangolo.com/).

## About this project

[👉 read here 👈](https://github.com/vvvvvvvector/SAT-solver-graphical-interface-client?tab=readme-ov-file#about-this-project)

## Running Locally

1. Open the project directory in a terminal

    ```sh
    cd project-name
    ```

2. Create a virtual environment:

   using python3:
   ```sh
   python3 -m venv venv
   ```

   or if you don't have python3:
   ```sh
   python -m venv venv
   ``` 

3. Run the virtual environment:

   MacOS:
   ```sh
   source venv/bin/activate
   ```

   Windows:
   ```sh
   source venv/Scripts/activate
   ```

   Linux (i don't know, haven't tried):
   ```sh
   source venv/???/activate
   ```

4. Check if it's running using following command:

    ```sh
    which python
    ```

    if everything is fine you are going to see a path for python in the virtual environment

5. Install dependencies:

    ```sh
    pip install -r requirements.txt
    ```

6. Start the development server:

    ```sh
    uvicorn main:app --port 8000 --reload
    ```

    this command will run the program on 8000 port, **don't change it**, this port is hardcoded on the [client-side](https://github.com/vvvvvvvector/SAT-solver-graphical-interface-client)
