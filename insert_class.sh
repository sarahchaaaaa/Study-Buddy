if [ $# -lt 2 ]; then
    echo "Not enough args, dude"
    exit 1
fi

cat <<EOF | sqlite3 database
insert into user_table
(CRN, NAME)
values
("$1", "$2")
EOF
