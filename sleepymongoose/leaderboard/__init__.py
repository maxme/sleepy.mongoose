from redis import Redis, ConnectionPool
from copy import deepcopy
from math import ceil

class Leaderboard(object):
    VERSION = '1.1.4'
    DEFAULT_PAGE_SIZE = 25
    DEFAULT_REDIS_HOST = 'localhost'
    DEFAULT_REDIS_PORT = 6379
    DEFAULT_REDIS_DB = 0

    @classmethod
    def pool(self, host, port, db, pools={}):
        """
        Fetch a redis conenction pool for the unique combination of host
        and port. Will create a new one if there isn't one already.
        """
        key = (host,port,db)
        rval = pools.get( key )
        if not isinstance(rval,ConnectionPool):
            rval = ConnectionPool(host=host, port=port, db=db)
            pools[ key ] = rval
        return rval

    def __init__(self, leaderboard_name, **options):
        """
        Initialize a connection to a specific leaderboard. By default, will use a
        redis connection pool for any unique host:port:db pairing.

        The options and their default values (if any) are:

        host : the host to connect to if creating a new handle ('localhost')
        port : the port to connect to if creating a new handle (6379)
        db : the redis database to connect to if creating a new handle (0)
        page_size : the default number of items to return in each page (25)
        connection : an existing redis handle if re-using for this leaderboard
        connection_pool : redis connection pool to use if creating a new handle
        """
        self.leaderboard_name = leaderboard_name
        self.options = deepcopy(options)

        self.page_size = self.options.pop('page_size', self.DEFAULT_PAGE_SIZE)
        if self.page_size < 1:
            self.page_size = self.DEFAULT_PAGE_SIZE

        self.redis_connection = self.options.pop('connection',None)
        if not isinstance(self.redis_connection,Redis):
            if 'connection_pool' not in self.options:
                self.options['connection_pool'] = self.pool(
                    self.options.pop('host', self.DEFAULT_REDIS_HOST),
                    self.options.pop('port', self.DEFAULT_REDIS_PORT),
                    self.options.pop('db', self.DEFAULT_REDIS_DB)
                )
            self.redis_connection = Redis(**self.options)

    def rank_uid(self, uid, score, level, name):
        self.redis_connection.set(self.leaderboard_name + ":" + uid + ":level", level)
        self.redis_connection.set(self.leaderboard_name + ":" + uid + ":name", name)
        return self.redis_connection.zadd(self.leaderboard_name, **{str(uid):score})

    def remove_uid(self, uid):
        return self.redis_connection.zrem(self.leaderboard_name, str(uid))

    def clear(self):
        '''Remove all rankings for this leaderboard.'''
        self.redis_connection.delete(self.leaderboard_name)

    def total_scores(self):
        return self.redis_connection.zcard(self.leaderboard_name)

    def total_pages(self, **options):
        return ceil(float(self.total_scores()) / options.get('page_size',self.page_size))

    def total_uids_in_score_range(self, min_score, max_score):
        return self.redis_connection.zcount(self.leaderboard_name, min_score, max_score)

    def change_score_for(self, uid, delta):
        return self.redis_connection.zincrby(self.leaderboard_name, str(uid), delta)

    def rank_for(self, uid, use_zero_index_for_rank = False):
        try:
            return self.redis_connection.zrevrank(self.leaderboard_name, str(uid))\
                + (0 if use_zero_index_for_rank else 1)
        except: return None

    def score_only_for(self, uid):
        return self.redis_connection.zscore(self.leaderboard_name, str(uid))

    def score_for(self, uid):
        level = self.redis_connection.get(self.leaderboard_name + ":" + uid + ":level")
        name = self.redis_connection.get(self.leaderboard_name + ":" + uid + ":name")
        score = self.redis_connection.zscore(self.leaderboard_name, str(uid))
        return score, level, name

    def check_uid(self, uid):
        return not None == self.redis_connection.zscore(self.leaderboard_name, str(uid))

    def score_and_rank_for(self, uid, use_zero_index_for_rank = False):
        return {
            'uid' : uid,
            'score' : self.score_for(uid),
            'rank' : self.rank_for(uid, use_zero_index_for_rank)
        }

    def remove_uids_in_score_range(self, min_score, max_score):
        return self.redis_connection.zremrangebyscore(self.leaderboard_name, min_score, max_score)

    def leaders(self, current_page, with_scores = True, with_rank = True, use_zero_index_for_rank = False, **options):
        if current_page < 1:
            current_page = 1

        page_size = options.get('page_size',self.page_size)
        tpages = self.total_pages(page_size=page_size)

        index_for_redis = current_page - 1

        starting_offset = (index_for_redis * page_size)
        if starting_offset < 0:
            starting_offset = 0

        ending_offset = (starting_offset + page_size) - 1

        raw_leader_data = self.redis_connection.zrevrange(self.leaderboard_name, int(starting_offset), int(ending_offset), with_scores)
        if raw_leader_data:
            return self._massage_leader_data(raw_leader_data, with_rank, use_zero_index_for_rank)
        else:
            return None

    def around_me(self, uid, with_scores = True, with_rank = True, use_zero_index_for_rank = False, **options):
        reverse_rank_for_uid = \
            self.redis_connection.zrevrank(self.leaderboard_name, str(uid))
        if not reverse_rank_for_uid:
            return None

        page_size = options.get('page_size', self.page_size)
        starting_offset = reverse_rank_for_uid - (page_size / 2)
        if starting_offset < 0:
            starting_offset = 0

        ending_offset = (starting_offset + page_size) - 1

        raw_leader_data = self.redis_connection.zrevrange(self.leaderboard_name, starting_offset, ending_offset, with_scores)
        if raw_leader_data:
            return self._massage_leader_data(raw_leader_data, with_rank, use_zero_index_for_rank)
        else:
            return None

    def ranked_in_list(self, uids, with_scores = True, use_zero_index_for_rank = False):
        ranks_for_uids = []

        for uid in uids:
            data = {}
            data['uid'] = uid
            data['rank'] = self.rank_for(uid, use_zero_index_for_rank)
            if with_scores:
                data['score'] = self.score_for(uid)

            ranks_for_uids.append(data)

        return ranks_for_uids

    def _massage_leader_data(self, leaders, with_rank, use_zero_index_for_rank):
        uid_attribute = True
        leader_data = []

        for leader_data_item in leaders:
            data = {}
            data['uid'] = leader_data_item[0]
            try:
                data['level'] = int(self.redis_connection.get(self.leaderboard_name + ":" + data['uid'] + ":level"))
            except:
                data['level'] = 0
            data['name'] = self.redis_connection.get(self.leaderboard_name + ":" + data['uid'] + ":name")
            try:
                data['score'] = int(leader_data_item[1])
            except:
                data['score'] = 0
            if with_rank:
                data['rank'] = self.rank_for(data['uid'], use_zero_index_for_rank)
            leader_data.append(data)

        return leader_data
