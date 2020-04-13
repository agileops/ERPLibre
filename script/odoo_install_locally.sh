#!/bin/bash
################################################################################
# Script for installing Odoo on Ubuntu 14.04, 15.04, 16.04 and 18.04 (could be used for other version too)
# Author: Yenthe Van Ginneken
#-------------------------------------------------------------------------------
# This script will install Odoo on your Ubuntu 16.04 server. It can install multiple Odoo instances
# in one Ubuntu because of the different xmlrpc_ports
#-------------------------------------------------------------------------------
# Make a new file:
# sudo nano odoo-install.sh
# Place this content in it and then make the file executable:
# sudo chmod +x odoo-install.sh
# Execute the script to install Odoo:
# ./odoo-install
################################################################################

. ./env_var.sh

OE_USER=$(whoami)
OE_HOME=$PWD
OE_HOME_EXT="${OE_HOME}/odoo"
# The default port where this Odoo instance will run under (provided you use the command -c in the terminal)
# Set to true if you want to install it, false if you don't need it or have it already installed.
#INSTALL_WKHTMLTOPDF="True"
# Set the default Odoo port (you still have to use -c /etc/odoo-server.conf for example to use this.)
#OE_PORT="8069"
#OE_LONGPOLLING_PORT="8072"
# Choose the Odoo version which you want to install. For example: 12.0, 11.0, 10.0 or saas-18. When using 'master' the master version will be installed.
# IMPORTANT! This script contains extra libraries that are specifically needed for Odoo 12.0
#OE_VERSION="stable_prod_12.0"
# set the superadmin password
#OE_SUPERADMIN="admin"
OE_CONFIG_FILE="${OE_HOME}/config.conf"
#OE_CONFIG="${OE_USER}"
#MINIMAL_ADDONS="False"
#INSTALL_NGINX="True"

echo -e "* Create server config file"

touch ${OE_CONFIG_FILE}
echo -e "* Creating server config file"
printf '[options] \n; This is the password that allows database operations:\n' > ${OE_CONFIG_FILE}
printf "admin_passwd = ${OE_SUPERADMIN}\n" >> ${OE_CONFIG_FILE}
printf "db_host = False\n" >> ${OE_CONFIG_FILE}
printf "db_port = False\n" >> ${OE_CONFIG_FILE}
printf "db_user = ${OE_USER}\n" >> ${OE_CONFIG_FILE}
printf "db_password = False\n" >> ${OE_CONFIG_FILE}
printf "xmlrpc_port = ${OE_PORT}\n" >> ${OE_CONFIG_FILE}
printf "longpolling_port = ${OE_LONGPOLLING_PORT}\n" >> ${OE_CONFIG_FILE}

printf "addons_path = ${OE_HOME_EXT}/addons,${OE_HOME}/addons/addons," >> ${OE_CONFIG_FILE}
printf "${OE_HOME}/addons/web," >> ${OE_CONFIG_FILE}
printf "${OE_HOME}/addons/santelibre," >> ${OE_CONFIG_FILE}
if [ $MINIMAL_ADDONS = "False" ]; then
    printf "${OE_HOME}/addons/account-analytic," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/account-budgeting," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/account-closing," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/account-consolidation," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/account-financial-reporting," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/account-financial-tools," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/account-fiscal-rule," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/account-invoice-reporting," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/account-invoicing," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/account-payment," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/account-reconcile," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/apps-store," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/bank-payment," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/bank-statement-import," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/brand," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/business-requirement," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/commission," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/community-data-files," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/connector-telephony," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/contract," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/credit-control," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/currency," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/data-protection," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/development," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/donation," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/e-commerce," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/edi," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/event," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/helpdesk," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/hr," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/knowledge," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/l10n-canada," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/maintenance," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/management-system," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/manufacture," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/margin-analysis," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/mis-builder," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/muk_base," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/muk_misc," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/muk_web," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/muk_website," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/multi-company," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/odoo-base-addons," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/odoo-business-spending-management-quebec-canada," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/odoo-entertainment-addons," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/odoo-git-addons," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/odoo-hr-addons," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/odoo-partner-addons," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/odoo-product-addons," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/odoo-project-addons," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/odoo-purchase-addons," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/odoo-stock-addons," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/odoo-survey-addons," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/odoo-timesheet-addons," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/odoo-web-addons," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/openeducat_erp," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/partner-contact," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/pos," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/product-attribute," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/product-pack," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/product-variant," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/project," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/project-reporting," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/purchase-workflow," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/quotation-revision," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/queue," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/reporting-engine," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/sale-workflow," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/scrummer," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/server-auth," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/server-brand," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/server-env," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/server-tools," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/server-ux," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/smile_addons," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/social," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/stock-logistics-warehouse," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/timesheet," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/website," >> ${OE_CONFIG_FILE}
    printf "${OE_HOME}/addons/wms," >> ${OE_CONFIG_FILE}
fi
printf "\n" >> ${OE_CONFIG_FILE}

printf "workers = 0\n" >> ${OE_CONFIG_FILE}
printf "max_cron_threads = 2\n" >> ${OE_CONFIG_FILE}

if [ ${INSTALL_NGINX} = "True" ]; then
    printf "xmlrpc_interface = 127.0.0.1\n" >> ${OE_CONFIG_FILE}
    printf "netrpc_interface = 127.0.0.1\n" >> ${OE_CONFIG_FILE}
    printf "proxy_mode = True\n" >> ${OE_CONFIG_FILE}
fi

echo -e "\n---- Create Virtual environment Python ----"
cd ${OE_HOME}
python3.7 -m venv venv
cd -

echo -e "\n---- Install python packages/requirements ----"
${OE_HOME}/venv/bin/pip3 install --upgrade pip
${OE_HOME}/venv/bin/pip3 install wheel
${OE_HOME}/venv/bin/pip3 install -r https://gitlab.com/mathbentech/odoo/raw/${OE_VERSION}/requirements.txt
${OE_HOME}/venv/bin/pip3 install phonenumbers
# For dev/testing
${OE_HOME}/venv/bin/pip3 install websocket-client

echo -e "\n---- Install Odoo with addons module ----"
git submodule update --init

echo -e "\n---- Add link dependency in site-packages of Python ----"
ln -fs ${OE_HOME_EXT}/odoo ${OE_HOME}/venv/lib/python3.7/site-packages/
ln -fs ${OE_HOME_EXT}/odoo ${OE_HOME}/venv/lib/python3.6/site-packages/
