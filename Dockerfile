FROM python:3.8-slim-buster
RUN pip install --no-cache-dir similar_documents
CMD ["bash"]