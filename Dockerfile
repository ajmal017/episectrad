FROM python

# TA-Lib
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
  tar -xvzf ta-lib-0.4.0-src.tar.gz && \
  cd ta-lib/ && \
  ./configure --prefix=/usr && \
  make && \
  make install

RUN rm -R ta-lib ta-lib-0.4.0-src.tar.gz

WORKDIR  /usr/src/app

RUN pip install TA-Lib==0.4.17 numpy==1.17.4 scipy==1.3.3 pandas==0.24.2

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000" ]
