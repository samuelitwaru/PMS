MUSER="$1"
MPASS="$2"
MDB="$3"
 
MHOST="localhost"
 
[ "$4" != "" ] && MHOST="$4"
 
# Detect paths
MYSQL=$(which mysql)
AWK=$(which awk)
GREP=$(which grep)

# make sure we can connect to server
$MYSQL -u $MUSER -p$MPASS -h $MHOST -e "use $MDB"  &>/dev/null
if [ $? -ne 0 ]
then
	echo "Error - Cannot connect to mysql server using given username, password or database does not exits!"
	exit 2
fi

# drop database
$MYSQL -u $MUSER -p$MPASS -h $MHOST $MDB -e "drop database $MDB; create database $MDB"
