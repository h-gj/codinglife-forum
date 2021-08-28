FROM 123123hgj/web_base:v1.0 
ADD . /var/www/flask
VOLUME ["/var/www/flask"]
WORKDIR /var/www/flask
EXPOSE 8080
CMD ["uwsgi", "uwsgi.ini"]
