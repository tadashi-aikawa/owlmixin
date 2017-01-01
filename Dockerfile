FROM python:3-onbuild

RUN pip update setuptools pip
RUN pip install wheel twine

CMD ["sh", "release.sh", ${VERSION}, ${PASSWORD}]
