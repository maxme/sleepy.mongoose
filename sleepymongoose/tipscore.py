import leaderboard
from datetime import datetime
from salt import *
import random
import re

try:
    import json
except ImportError:
    import simplejson as json

MAX_PAGE_SIZE = 100

class TipScoreHandler:
    tsh = None
    def __init__(self):
        pass

    def check_args(self, args, checks, salt=False):
        for i in checks:
            if not i in args:
                print i, " not in args"
                return '{"error": %d}' % (1)
        if salt:
            if not "salt" in args:
                return '{"error": %d}' % (1)
            if not is_salt_valid(args["salt"]):
                return '{"error": %d}' % (5)
        return None


    def __get_leaderboard(self, lid):
        return leaderboard.Leaderboard(lid)

    def _get_leaderboard(self, args, out):
        check_res = self.check_args(args, ["leaderboard_id"])
        if check_res:
            out(check_res)
            return
        leaderboard = self.__get_leaderboard(args["leaderboard_id"])
        count = leaderboard.total_scores()
        res = {
            "ok": 1,
            "count": count,
            "leaderboard_id": args["leaderboard_id"]
            }
        out(json.dumps(res))

    def _put_score(self, args, out):
        check_res = self.check_args(args, ["leaderboard_id", "name", "id", "score", "level"], salt=True)
        if check_res:
            out(check_res)
            return
        # FIXME must check signature
        try:
            score = int(args["score"])
            level = int(args["level"])
            name = args["name"]
            leaderboard_id = args["leaderboard_id"]
            leaderboard = self.__get_leaderboard(leaderboard_id)
            cur_score = leaderboard.score_only_for(args["id"])
            res = 1
            rank = 0
            if not cur_score or score > cur_score:
                leaderboard.rank_uid(args["id"], score, level, name)
                rank = leaderboard.rank_for(args["id"])
                res = 2
            else:
                rank = leaderboard.rank_for(args["id"])
            out(json.dumps({"ok": res, "rank": rank}))
        except Exception as e:
            print e
            out(json.dumps({"error": -1}))

    def _get_scores(self, args, out):
        check_res = self.check_args(args, ["leaderboard_id", "id", "page_size"])
        if check_res:
            out(check_res)
            return
        page_size = min(MAX_PAGE_SIZE, int(args["page_size"]))
        # get user score
        leaderboard = self.__get_leaderboard(args["leaderboard_id"])
        scores = leaderboard.around_me(args["id"], page_size=page_size)
        if not scores:
            out(json.dumps({"error": 8}))
            return
        res = {"ok": 1, "scores": scores}
        out(json.dumps(res))

    def _get_score_page(self, args, out):
        check_res = self.check_args(args, ["leaderboard_id", "start", "page_size"])
        if check_res:
            out(check_res)
            return
        page_size = min(MAX_PAGE_SIZE, int(args["page_size"]))
        leaderboard = self.__get_leaderboard(args["leaderboard_id"])
        scores = leaderboard.leaders(int(args["start"]), page_size=page_size)
        res = {"ok": 1, "scores": scores}
        out(json.dumps(res))

    def _get_rank(self, args, out):
        check_res = self.check_args(args, ["leaderboard_id", "id"])
        if check_res:
            out(check_res)
            return
        rank = leaderboard.rank_for(args["id"])
        out(json.dumps({"rank": rank}))

# Errors
#-1 - undefined
# 1 - invalid post data
# 2 - user asks for his own code
# 3 - code has been used too many times
# 4 - invalid code
# 5 - invalid salt
# 6 - salt already used with this code
# 7 - invalid leaderboard
# 8 - can't get scores around this id

def write(x):
    import sys
    sys.stdout.write(x + "\n")

def dummy_write(x):
    pass

def test_gendata(n):
    import random
    tsh = TipScoreHandler.tsh = TipScoreHandler()
    for i in range(n):
        test_putscore(dummy_write)

def test_getscores():
    tsh = TipScoreHandler.tsh = TipScoreHandler()
    #tsh._get_leaderboard({"leaderboard_id": "12"}, write)
    tsh._get_scores( {"leaderboard_id": "12", "id": "id36730657", "page_size": 5}, write)

def test_getleaderboard():
    tsh = TipScoreHandler.tsh = TipScoreHandler()
    tsh._get_leaderboard( {"leaderboard_id": "12"}, write)

def test_putscore(w):
    tsh = TipScoreHandler.tsh = TipScoreHandler()
    tsh._put_score({
        "name": random.choice(["bob", "robert", "rene", "pouet"]) + str(random.randint(1, 12321)),
        "score": random.randint(1, 1000),
        "level": random.randint(1, 50),
        "id": "id" + str(random.randint(1, 100000000)),
        "salt": "103950784",
        "leaderboard_id": "12"
        }, w)

def test_putscore2(w, id):
    tsh = TipScoreHandler.tsh = TipScoreHandler()
    tsh._put_score({
        "name": random.choice(["bob", "robert", "rene", "pouet"]) + str(random.randint(1, 12321)),
        "score": random.randint(1, 1000),
        "level": random.randint(1, 50),
        "id": id,
        "salt": "103950784",
        "leaderboard_id": "12"
        }, w)


if __name__ == "__main__":
    test_getscores()
    #test_putscore2(write, "pouet5")
    #test_getleaderboard()
    #test_gendata(1000)



