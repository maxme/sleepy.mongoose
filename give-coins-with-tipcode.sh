TIPCODE="$1"

salts="427432462 183942696 988883703 344385654 885483173 464060285 338279171 424980788 842410161 764781904"

for i in $salts; do
    echo $i
    curl --data "id=$RANDOM;salt=$i;tipcode=$TIPCODE" http://gameboy.iopixel.com/mongodb/tipcode/_get
done

