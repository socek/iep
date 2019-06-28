FROM python:3.7

# Configuration
ENV PYTHONUNBUFFERED 1
ENV EGG_INFO_NAME Imladris_Event_Planner
ENV APP_DIR /code
ENV USER_DIR /home/user

# Create dev user
RUN useradd -U user && mkdir -p $USER_DIR && chown user:user $USER_DIR && chmod 777 $USER_DIR

# Create code dir
WORKDIR $APP_DIR
RUN chmod 777 $APP_DIR

# Install pipenv. Pipenv is a better then pip tool for managing packages.
RUN pip install pipenv

# Install dependencies
USER user
COPY --chown=user:user bashrc /home/user/.bashrc
COPY --chown=user:user code/Pipfile $APP_DIR
COPY --chown=user:user code/Pipfile.lock $APP_DIR
RUN pipenv install --dev

# Copy all the code and run setuo.py
COPY --chown=user:user code $APP_DIR
RUN pipenv run python setup.py develop

CMD ./start.sh
EXPOSE 18765
