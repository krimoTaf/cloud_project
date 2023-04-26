FROM python:3-alpine

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt ./

RUN pip install -r requirements.txt

# Bundle app source
COPY . .

CMD flask --app tcb init-db;gunicorn -w 4 -b 0.0.0.0:5000 'tcb:create_app()'



EXPOSE 3000
