for i in {1..16}
do
    curl \
    "http://fantasydata.com/nfl-stats/nfl-fantasy-football-stats.aspx?fs=1&stype=0&sn=1&w=$i&s=&t=0&p=5&st=FantasyPointsPPR&d=1&ls=FantasyPointsPPR&live=false" \
    -o te$i.html
done
