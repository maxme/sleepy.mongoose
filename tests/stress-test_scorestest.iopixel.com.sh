#define CAREER_SCORE_LBID                   "874496"
#define TWOMN_SCORE_LBID                    "745187"
#define FIVEMN_SCORE_LBID                   "896367"
#define NETWORK_SCORE_LBID                  "896377"

LEADERBOARD_ID=874496

for i in $(seq 0 $1); do
    echo "id=$RANDOM&leaderboard_id=$LEADERBOARD_ID&salt=103950784&score=$RANDOM&name=bob$RANDOM&level=$(($RANDOM % 50))"
done | xargs -P $2 -I {} curl --data "{}" http://mdrive.iopixel.com/mongodb/tipscore/_put_score

