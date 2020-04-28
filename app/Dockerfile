FROM python:3.8.2

WORKDIR /usr/src/papers-library

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

# RUN pip install torch===1.4.0 torchvision===0.5.0 -f https://download.pytorch.org/whl/torch_stable.html

ADD ./requirements.txt ./

RUN pip install -r requirements.txt

ADD . .

CMD ["python", "./src/main.py"]