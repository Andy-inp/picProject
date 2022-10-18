FROM python:3.10

# Set an environment variable
ENV APP /app
#ENV PROJECT_ENV prod
ENV EXPOSE_PORT 8080
ENV PIP_ROOT_USER_ACTION=ignore

# Create the directory
RUN groupadd -g 1001 -r tomcat && useradd -r -u 1001 -g tomcat tomcat
RUN mkdir $APP && chown tomcat.tomcat $APP
WORKDIR $APP

# Copy the requirements file in order to install
# Python dependencies
COPY --chown=tomcat:tomcat . .
COPY APP-META/docker-entrypoint.sh /bin/docker-entrypoint.sh
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Expose the port uWSGI will listen on
EXPOSE ${EXPOSE_PORT}

# We copy the rest of the codebase into the image


# Finally, we run uWSGI with the ini file
USER tomcat
ENTRYPOINT ["/bin/docker-entrypoint.sh"]
CMD ["runserver"]
