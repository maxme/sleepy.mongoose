CAREER_SCORE_LBID=874496
TWOMN_SCORE_LBID=745187
FIVEMN_SCORE_LBID=896367
NETWORK_SCORE_LBID=896377

LEADERBOARD_ID=$CAREER_SCORE_LBID
MAX_SCORE=39000
for i in $(seq 1 $1); do
    level=$(($RANDOM % 50))
    score=$(($(($RANDOM * $RANDOM % $MAX_SCORE)) * $level))
    name=$(head -n $(($RANDOM%$(wc -l < nicknames.txt))) nicknames.txt| tail -n 1)
    echo "id=$RANDOM&leaderboard_id=$LEADERBOARD_ID&salt=103950784&score=$score&name=$name&level=$level"
done | xargs -P $2 -I {} curl --data "{}" http://mdrive.iopixel.com/mongodb/tipscore/_put_score


LEADERBOARD_ID=$TWOMN_SCORE_LBID
MAX_SCORE=20000
for i in $(seq 1 $1); do
    level=$(($RANDOM % 50))
    score=$(($(($RANDOM * $RANDOM % $MAX_SCORE)) * $level))
    name=$(head -n $(($RANDOM%$(wc -l < nicknames.txt))) nicknames.txt| tail -n 1)
    echo "id=$RANDOM&leaderboard_id=$LEADERBOARD_ID&salt=103950784&score=$score&name=$name&level=$level"
done | xargs -P $2 -I {} curl --data "{}" http://mdrive.iopixel.com/mongodb/tipscore/_put_score

LEADERBOARD_ID=$FIVEMN_SCORE_LBID
MAX_SCORE=80000
for i in $(seq 1 $1); do
    level=$(($RANDOM % 50))
    score=$(($(($RANDOM * $RANDOM % $MAX_SCORE)) * $level))
    name=$(head -n $(($RANDOM%$(wc -l < nicknames.txt))) nicknames.txt| tail -n 1)
    echo "id=$RANDOM&leaderboard_id=$LEADERBOARD_ID&salt=103950784&score=$score&name=$name&level=$level"
done | xargs -P $2 -I {} curl --data "{}" http://mdrive.iopixel.com/mongodb/tipscore/_put_score

LEADERBOARD_ID=$NETWORK_SCORE_LBID
MAX_SCORE=19000
for i in $(seq 1 $1); do
    level=$(($RANDOM % 50))
    score=$(($RANDOM * $RANDOM % $MAX_SCORE))
    name=$(head -n $(($RANDOM%$(wc -l < nicknames.txt))) nicknames.txt| tail -n 1)
    echo "id=$RANDOM&leaderboard_id=$LEADERBOARD_ID&salt=103950784&score=$score&name=$name&level=$level"
done | xargs -P $2 -I {} curl --data "{}" http://mdrive.iopixel.com/mongodb/tipscore/_put_score

