CAREER_SCORE_LBID=874496
TWOMN_SCORE_LBID=745187
FIVEMN_SCORE_LBID=896367
NETWORK_SCORE_LBID=896377


# ARGS
MODE=$CAREER_SCORE_LBID
SMIN=8000000
SMAX=100000000

if [ $SMIN -le 5000000 ]; then
    echo "mininum <$SMIN> seems strange"
fi

echo "zremrangebyscore $MODE $SMIN $SMAX" | redis-cli