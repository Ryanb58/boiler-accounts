FROM python:3.7

ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
RUN rm app.sqlite || true

EXPOSE 22222
RUN python create_tables.py
RUN python create_user.py
CMD ["python", "-u", "app.py"]