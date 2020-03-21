FROM python:alpine 

RUN pip install flask
RUN mkdir app
WORKDIR /app/
COPY app.py .

CMD ["flask", "run" ,"--host=0.0.0.0"]