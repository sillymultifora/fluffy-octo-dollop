FROM pytorch/pytorch:2.4.0-cuda12.1-cudnn9-devel

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git
    
RUN git clone https://github.com/sillymultifora/fluffy-octo-dollop.git
RUN cd fluffy-octo-dollop
RUN pip install -r requirements.txt

CMD bash ./start_servers.sh