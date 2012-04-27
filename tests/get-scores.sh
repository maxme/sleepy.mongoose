HOST=scores.iopixel.com/mongodb
#HOST=scorestest.iopixel.com/mongodb
#HOST=mdrive.iopixel.com/mongodb
#HOST=localhost:27080

CAREER_SCORE_LBID=874496
TWOMN_SCORE_LBID=745187
FIVEMN_SCORE_LBID=896367
NETWORK_SCORE_LBID=896377

#curl --data "id=idquinexistepas&leaderboard_id=$CAREER_SCORE_LBID&salt=103950784&page_size=10" http://$HOST/tipscore/_get_scores
#echo
#curl --data "id=pouet5&leaderboard_id=$CAREER_SCORE_LBID&salt=103950784&page_size=100" http://$HOST/tipscore/_get_scores
#echo
#curl --data "id=pouet5&leaderboard_id=$CAREER_SCORE_LBID&salt=103950784&page_size=1" http://$HOST/tipscore/_get_scores
#echo
#curl --data "id=pouet5&leaderboard_id=$CAREER_SCORE_LBID&salt=103950784&page_size=2" http://$HOST/tipscore/_get_scores
#echo
#curl --data "id=pouet5&leaderboard_id=$CAREER_SCORE_LBID&salt=103950784&page_size=3" http://$HOST/tipscore/_get_scores
#echo
#curl --data "id=pouet5&leaderboard_id=$CAREER_SCORE_LBID&salt=103950784&page_size=4" http://$HOST/tipscore/_get_scores

echo
echo "10 first scores"
curl --data "leaderboard_id=$CAREER_SCORE_LBID&page_size=1000&start=0" http://$HOST/tipscore/_get_score_page
