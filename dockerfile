FROM pytorch/pytorch:2.4.1-cuda12.1-cudnn9-devel

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

RUN git clone https://github.com/sillymultifora/fluffy-octo-dollop.git
RUN cd fluffy-octo-dollop
RUN pip install -r requirments.txt

CMD ./start_servers.sh