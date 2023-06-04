FROM ubuntu:16.04
# FROM debian:buster
# FROM debian:jessie
# MAINTAINER Odoo S.A. <info@odoo.com>

# Install some deps, lessc and less-plugin-clean-css, and wkhtmltopdf
RUN set -x; \
        apt-get update \
        && apt-get upgrade -y \
        && apt-get install -y --no-install-recommends \
            curl \
            wget \
            git \
            python-pip \
            gdebi-core \
            python-dateutil \
            python-feedparser \
            python-ldap \
            python-libxslt1 \
            python-lxml \
            python-mako \
            python-openid \
            python-psycopg2 \
            python-pybabel \
            python-pychart \
            python-pydot \
            python-pyparsing \
            python-reportlab \
            python-simplejson \
            python-tz \
            python-vatnumber \
            python-vobject \
            python-webdav \
            python-werkzeug \
            python-xlwt \
            python-yaml \
            python-zsi \
            python-docutils \
            python-psutil \
            python-mock \
            python-unittest2 \
            python-jinja2 \
            python-pypdf \
            python-decorator \
            python-requests \
            python-passlib \
            python-pil \
            python-suds 
            # ca-certificates \
            # curl \
            # node-less \
            # python-gevent \
            # python-pip \
            # python-renderpm \
            # python-support 
            # python-watchdog \
        # && curl -o wkhtmltox.deb -SL https://downloads.wkhtmltopdf.org/0.12/0.12.1/wkhtmltox-0.12.1_linux-trusty-amd64.deb \
        # && echo '40e8b906de658a2221b15e4e8cd82565a47d7ee8 wkhtmltox.deb' | sha1sum -c - \
        # && dpkg --force-depends -i wkhtmltox.deb \
        # && apt-get -y install -f --no-install-recommends \
        # && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false -o APT::AutoRemove::SuggestsImportant=false npm \
        # && rm -rf /var/lib/apt/lists/* wkhtmltox.deb \
        # && pip install psycogreen==1.0

# Install wkhtmltopdf
RUN curl -o wkhtmltox.deb -SL https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.1/wkhtmltox-0.12.1_linux-trusty-amd64.deb \
    && dpkg --force-depends -i wkhtmltox.deb \
    && apt-get -y install -f --no-install-recommends \
    && rm wkhtmltox.deb

# Install odoo
RUN curl -o odoo.deb -SLk https://nightly.odoo.com/10.0/nightly/deb/odoo_10.0.20170101_all.deb \
    && dpkg --force-depends -i odoo.deb \
    && apt-get -y install -f --no-install-recommends \
    && rm odoo.deb

RUN curl --insecure https://bootstrap.pypa.io/pip/2.7/get-pip.py -o get-pip.py \
    && python get-pip.py --force-reinstall \
    && python -m pip install --upgrade "pip < 21.0"

RUN pip install \
    num2words \
    PyPDF2 \
    gdata \
    psycogreen \
    ofxparse \
    XlsxWriter \
    xlrd

RUN apt-get install -y \
    node-clean-css \
    node-less \
    python-gevent

# Copy entrypoint script and Odoo configuration file
COPY ./entrypoint.sh /
COPY ./etc/odoo.conf /etc/odoo/
RUN chown odoo /etc/odoo/odoo.conf
RUN chown odoo /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Mount /var/lib/odoo to allow restoring filestore and /mnt/extra-addons for users addons
RUN mkdir -p /mnt/extra-addons \
        && chown -R odoo /mnt/extra-addons

RUN mkdir -p /var/lib/odoo/.local/share && \
    chown -R odoo:odoo /var/lib/odoo


# /etc/odoo for config and log files
VOLUME ["/var/lib/odoo", "/mnt/extra-addons", "/etc/odoo"]

# Expose Odoo services
EXPOSE 8069 8071 8072

# Set the default config file
ENV ODOO_RC /etc/odoo/odoo.conf

# Set default user when running the container
# TODO: find a way to use odoo insted
USER root

ENTRYPOINT ["/entrypoint.sh"]
CMD ["odoo"]