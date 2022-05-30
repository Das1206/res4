FROM python:3.8

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
RUN python3 -m nltk.downloader pros_cons
RUN python3 -m nltk.downloader wordnet
RUN python3 -m nltk.downloader reuters
RUN python3 -m nltk.downloader stopwords
RUN python3 -m nltk.downloader averaged_perceptron_tagger

EXPOSE 5000

CMD ["python", "main.py"]