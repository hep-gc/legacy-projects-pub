FROM danikam/csv2_private_web:190110

USER root

WORKDIR /jobs

ADD init_setup.sh /jobs

# Install supervisor
RUN easy_install supervisor

# Add supervisor's configuration file to the container. Note: This config file is referred by supervisord once started inside container
COPY supervisord.conf /usr/etc/supervisord.conf

# Expose needed ports
EXPOSE 80 443 444 3306 947 9618
EXPOSE 40000-40500

# Execute supervisord as entrypoint into the container
CMD ["/usr/bin/supervisord"]