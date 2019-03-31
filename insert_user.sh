if [ $# -lt 3 ]; then
    echo "Not enough args, dude"
    exit 1
fi

cat <<EOF | sqlite3 database
insert into user_table
(NETID, NAME, MAJOR)
values
("$1", "$2", "$3")
EOF
