use tipcode;

m = function(){
    emit("use_count", { count: this.use_count });
};

// reduce function
r = function(key , values) {
    var total = 0;
    for (var i=0; i<values.length; i++ )
        total += values[i].count;
    return { count : total };
};

res = db.codes.mapReduce(m, r, { out : "myout" });

db.myout.find();
db.myout.drop();

