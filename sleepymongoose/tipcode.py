from pymongo import uri_parser, connection, Connection, ASCENDING, DESCENDING
from pymongo.son import SON
from pymongo.errors import ConnectionFailure, ConfigurationError, OperationFailure, AutoReconnect
from bson import json_util
from salt import *
import random
import re

try:
    import json
except ImportError:
    import simplejson as json

MAX_TIPCODE_USAGE = 5

class TipCodeHandler:
    tch = None
    def __init__(self):
        self.conn = Connection("localhost", 27017)
        self.db = self.conn.tipcode
        self.codes = self.db.codes
        self.salts = self.db.salts
        self.freestuff = self.db.freestuff
        self.tokens = self.db.tokens

    def _generate_tipcode(self, call):
        maxchar = 5
        if (call >= 3):
            maxchar = 6
        if (call >= 5):
            maxchar = 7
        maxi = ord("9") - ord("0") + ord("z") - ord("a") + 1
        res = ""
        for i in range(maxchar):
            c = ord("o")
            while c == ord("o"):
                m = random.randint(1, maxi)
                if (m <= 9):
                    c = ord("0") + m
                else:
                    c = ord("a") + m - 10
            res += chr(c)
        return res

    def generate_tipcode(self):
        notnew = False
        i = 0
        while notnew == False and i < 20:
            i += 1
            tipcode = self._generate_tipcode(i)
            if self.codes.find({"tipcode": tipcode}).count() == 0:
                return tipcode.upper()
        return "0"

    def _create(self, args, out):
        if not(args["id"] and args["salt"]):
            out('{"error": %d}' % (1))
            return
        if not is_salt_valid(args["salt"]):
            out('{"error": %d}' % (5))
            return
        # Check if it has been generated
        cur = self.codes.find_one({"id": args["id"], "salt": args["salt"]})
        if cur:
            tipcode = cur["tipcode"]
            use_count = min(cur["use_count"], MAX_TIPCODE_USAGE)
            out('{"tipcode": "%s", "use_count": %d}' % (tipcode, use_count))
        else:
            # Else generate tipcode and save it to the db
            tipcode = self.generate_tipcode()
            doc = {"id": args["id"], "salt": args["salt"], "tipcode": tipcode, "use_count": 0}
            self.codes.save(doc)
            out('{"tipcode": "%s", "use_count": %d}' % (tipcode, 0))

    def _get(self, args, out):
        if not(args["id"] and args["salt"] and args["tipcode"]):
            out('{"error": %d}' % (1))
            return
        if not is_salt_valid(args["salt"]):
            out('{"error": %d}' % (5))
            return
        args["tipcode"] = args["tipcode"].upper()
        cur = self.codes.find_one({"tipcode": args["tipcode"]})
        if cur:
            tipcode = cur["tipcode"].upper()
            use_count = min(cur["use_count"], MAX_TIPCODE_USAGE)
            if args["id"] == cur["id"]:
                out('{"error": %d}' % (2))
            else:
                if use_count >= MAX_TIPCODE_USAGE:
                    out('{"error": %d}' % (3))
                else:
                    for code in self.salts.find({"tipcode": tipcode}):
                        if args["salt"] == code["salt"]:
                            out('{"error": %d}' % (6))
                            return
                    self.salts.save({"tipcode":tipcode, "salt": args["salt"]})
                    cur["use_count"] += 1
                    self.codes.save(cur)
                    out('{"ok": 1}')
        else:
            out('{"error": %d}' % (4))

    def _isfree(self, args, out):
        if not(args["id"] and args["salt"]):
            out('{"error": %d}' % (1))
            return
        if not is_salt_valid(args["salt"]):
            out('{"error": %d}' % (5))
            return
        cur = self.freestuff.find_one()
        if cur == None:
            out('{"ok": 0}')
        else:
            sig = sign_message('{"ok": 1, "coins": %d, "message": "%s"}' % (cur["coins"], cur["message"]))
            out('{"ok": 1, "coins": %d, "message": "%s", "platform": "%s", "sig": "%s"}' % (cur["coins"], cur["message"], cur["platform"], sig))


    def _token(self, args, out):
        if "token" in args:
            self.tokens.save({"token": args["token"]})
            out('{"ok": 1}')
        else:
            out('{"error": 1}')

# Errors
# 1 - invalid post data
# 2 - user asks for his own code
# 3 - code has been used too many times
# 4 - invalid code
# 5 - invalid salt
# 6 - salt already used with this code

if __name__ == "__main__":
    import sys
    tch = TipCodeHandler.tch = TipCodeHandler()
    print tch.is_salt_valid("103950784")
    print tch.is_salt_valid("103951783")
    print tch.sign_message('{"ok": 1, "coins": 123123, "message": "yo"}')
    ## out = sys.stdout.write
    ## tch.create({"id": "123", "salt": "123"}, out)
    ## out("\n")
    ## tch.create({"id": "123toto", "salt": "123"}, out)
    ## out("\n")
    ## tch.create({"id": "123", "salt": "124"}, out)
    ## out("\n")


