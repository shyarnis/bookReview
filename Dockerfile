# set base image
FROM python:3.11

# set environemnt variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# set the working directory to /app in the container
WORKDIR /app

# copy the requirements.txt file into directory /app in the container
COPY requirements.txt .

# upgrade pip to latest version to avoid error
RUN pip install --upgrade pip

# install the project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy all project files and folders into /app container
COPY . .

# make the entrypoint.sh executable
RUN chmod +x entrypoint.sh

# set the entrypoint
ENTRYPOINT [ "./entrypoint.sh" ]

# run the django application
# CMD [ "python", "manage.py", "runserver", "localhost:8000" ]
CMD [ "python", "manage.py", "runserver"]
