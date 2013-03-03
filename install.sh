# show all commands
set -v

sudo aptitude install gammu python-gammu
sudo aptitude install postgresql
sudo aptitude install python-pip

# create postgres user with the current name
sudo -u postgres createuser `whoami` -s
# set a postgres password
psql -c "alter user `whoami` password '`whoami`'"

# create gps_sms database
createdb gps_sms

# now do the python requirements
sudo pip install -r requirements.txt
