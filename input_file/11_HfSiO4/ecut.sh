#!/bin/bash
for ex in 90 100;
do
    etg1=$ex
    etg2=`expr 8 \* $ex`
    title=scf-ecut_$ex
    cat hfsio4.scf.in | sed -e "s/tgt1/$etg1/g" -e "s/tgt2/$etg2/g" > $title.in
    pw.x < $title.in | tee $title.out
done

grep '!' scf-ecut_*.out | awk '{print $1, $5}' | sed -e 's/scf-ecut_//g' -e 's/.out:!!//g' > scf-ecut_energy.dat

