FROM python:3.6-onbuild

RUN pip install -U setuptools pip wheel twine

CMD ["sh", "release.sh"]
