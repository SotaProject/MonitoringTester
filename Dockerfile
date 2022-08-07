FROM python:3.10

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt ./

RUN pip install -r requirements.txt

# Bundle app source
COPY main.py ./

CMD [ "python", "main.py" ]