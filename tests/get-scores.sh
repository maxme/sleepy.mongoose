
curl --data "id=idquinexistepas&leaderboard_id=12&salt=103950784&page_size=10" http://localhost:27080/tipscore/_get_scores
echo
curl --data "id=pouet5&leaderboard_id=12&salt=103950784&page_size=100" http://localhost:27080/tipscore/_get_scores
echo
curl --data "id=pouet5&leaderboard_id=12&salt=103950784&page_size=1" http://localhost:27080/tipscore/_get_scores
echo
curl --data "id=pouet5&leaderboard_id=12&salt=103950784&page_size=2" http://localhost:27080/tipscore/_get_scores
echo
curl --data "id=pouet5&leaderboard_id=12&salt=103950784&page_size=3" http://localhost:27080/tipscore/_get_scores
echo
curl --data "id=pouet5&leaderboard_id=12&salt=103950784&page_size=4" http://localhost:27080/tipscore/_get_scores

echo
echo "10 first scores"
curl --data "leaderboard_id=12&page_size=10&start=0" http://localhost:27080/tipscore/_get_score_page
