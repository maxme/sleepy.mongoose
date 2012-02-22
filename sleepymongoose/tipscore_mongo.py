from pymongo import uri_parser, connection, Connection, ASCENDING, DESCENDING
from pymongo.son import SON
from pymongo.errors import ConnectionFailure, ConfigurationError, OperationFailure, AutoReconnect
from datetime import datetime
from bson import json_util
from salt import *
import random
import re

try:
    import json
except ImportError:
    import simplejson as json

MAX_TIPCODE_USAGE = 5
MAX_BEFORE_AFTER = 50

class TipScoreHandler:
    tsh = None
    def __init__(self):
        self.conn = Connection("localhost", 27017)
        self.db = self.conn.tipscore
        self.scores = self.db.scores

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
        return eval("self.db.leaderboard_" + str(lid))

    def _get_leaderboard(self, args, out):
        check_res = self.check_args(args, ["leaderboard_id"])
        if check_res:
            out(check_res)
            return
        leaderboard_id = args["leaderboard_id"]
        collection = self.__get_leaderboard(leaderboard_id)
        count = collection.count()
        ## cur = self.db.leaderboards.find_one({"leaderboard_id": leaderboard_id})
        ## if not cur:
        ##     out('{"error": %d}' % (7))
        ##     return
        res = {
            "ok": 1,
            "count": count,
            "leaderboard_id": leaderboard_id
            }
        out(json.dumps(res))

    def _put_score(self, args, out):
        check_res = self.check_args(args, ["leaderboard_id", "name", "id", "score", "level"], salt=True)
        if check_res:
            out(check_res)
            return
        # FIXME must check signature
        leaderboard_id = args["leaderboard_id"]
        collection = self.__get_leaderboard(leaderboard_id)
        scoredoc = collection.find_one({"id": args["id"]})
        # ensure INT
        args["score"] = int( args["score"])
        args["level"] = int(args["level"])
        if scoredoc:
            if args["score"] > scoredoc["score"]:
                scoredoc["score"] = args["score"]
                scoredoc["name"] = args["name"]
                scoredoc["level"] = args["level"]
                scoredoc["timestamp"] = datetime.now()
                collection.save(scoredoc)
                out(json.dumps({"ok": 2}))
            else:
                out(json.dumps({"ok": 3}))
        else:
            doc = { "id": args["id"],
                    "name": args["name"],
                    "score": args["score"],
                    "level": args["level"],
                    "timestamp": datetime.now(),
                    }
            collection.save(doc)
            out(json.dumps({"ok": 1}))

    def __create_score_list(self, cursor, start, user_score):
        scores = []
        n = start
        ne = start
        oldscore = 0
        for i in cursor:
            n += 1
            if oldscore != i["score"]:
                oldscore = i["score"]
                ne = n
            if user_score and i["id"] == user_score["id"]:
                user_score["rank"] = ne
            scores.append((ne, i["level"], i["name"], i["score"]))
        return scores

    def _get_scores(self, args, out):
        check_res = self.check_args(args, ["leaderboard_id", "id", "nbefore", "nafter"])
        if check_res:
            out(check_res)
            return
        nbefore = min(MAX_BEFORE_AFTER, int(args["nbefore"]))
        nafter = min(MAX_BEFORE_AFTER,int(args["nafter"]))
        # get user score
        collection = self.__get_leaderboard(args["leaderboard_id"])
        user_score = collection.find_one({"id": args["id"]})
        score = user_score["score"]
        count = collection.find({"score": {"$gt": user_score["score"]}}, []).count()
        start = count - nbefore
        end = count + nafter + 1
        # get before / after scores
        cursor = collection.find({}, {"id", "level", "name", "score"}).sort("score", DESCENDING)\
                 .skip(count - nbefore).limit(nbefore + nafter + 1)
        scores = self.__create_score_list(cursor, start, user_score)
        res = {"user_score": [user_score["rank"], user_score["level"], user_score["name"], user_score["score"]],
               "scores": scores}
        out(json.dumps(res))

    def _get_scores_page(self, args, out):
        check_res = self.check_args(args, ["leaderboard_id", "start", "size"])
        if check_res:
            out(check_res)
            return
        size = min(MAX_BEFORE_AFTER, int(args["size"]))
        start = int(args["start"])
        cursor = collection.find({}, {"id", "level", "name", "score"}).sort("score", DESCENDING)\
                 .skip(start).limit(size)
        scores = self.__create_score_list(cursor, start, None)
        res = {"scores": scores}
        out(json.dumps(res))

    def _get_rank(self, args, out):
        check_res = self.check_args(args, ["leaderboard_id", "id"])
        if check_res:
            out(check_res)
            return

# Errors
# 1 - invalid post data
# 2 - user asks for his own code
# 3 - code has been used too many times
# 4 - invalid code
# 5 - invalid salt
# 6 - salt already used with this code
# 7 - invalid leaderboard

def write(x):
    import sys
    sys.stdout.write(x + "\n")

def dummy_write(x):
    pass

def test_gendata(n):
    import random
    tsh = TipScoreHandler.tsh = TipScoreHandler()
    for i in range(n):
        tsh._put_score({
            "name": random.choice(["bob", "robert", "rene", "pouet"]) + str(random.randint(1, 12321)),
            "score": random.randint(1, 1000000000),
            "level": random.randint(1, 50),
            "id": "id" + str(random.randint(1, 100000000)),
            "salt": "103950784",
            "leaderboard_id": "12"
            }, dummy_write)


def test_getscores():
    tsh = TipScoreHandler.tsh = TipScoreHandler()
    #tsh._get_leaderboard({"leaderboard_id": "12"}, write)
    tsh._get_scores( {"leaderboard_id": "12", "id": "id225807456", "nbefore": 15, "nafter": 15}, write)


if __name__ == "__main__":
    test_getscores()
    #test_gendata(1000000)


