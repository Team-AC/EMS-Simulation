# pull official base image
FROM python:3.9

# set working directory
WORKDIR /simulation

# install dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . ./

# Run Simulation
CMD python simulation.py