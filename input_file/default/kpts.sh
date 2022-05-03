#!/bin/bash
for kpt in 2 3 4 5 6 7 8;
do
    ktg=$kpt
    title=kpts_$kpt
    cat kpts.in | sed -e "s/ktg/$ktg/g" > $title.in
    pw.x < $title.in | tee $title.out
done

grep ! kpts_*.out | awk '{print $1, $5}' | sed -e 's/kpts_//g' -e 's/.out:!//g' > kpts_energy.dat

grep highest kpts_*.out | awk '{print $1, $8, $9}' | sed -e 's/kpts_//g' -e 's/.out://g' > kpts_band.dat
