# 
FROM python:3.9

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./ /code/

ENV API_KEY=api-API_KEY

# 
CMD ["uvicorn", "app_fast:app", "--host", "0.0.0.0", "--port", "80"]
