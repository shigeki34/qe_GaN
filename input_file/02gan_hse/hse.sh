#!/bin/bash
for qx in 1 2 4;
do
    qtg=$qx
    title=scf-hse_$qx
    cat scf-hse.in | sed -e "s/qtg/$qtg/g" > $title.in
    pw.x < $title.in | tee $title.out
done

grep '!!' scf-hse_*.out | awk '{print $1, $5}' | sed -e 's/scf-hse_//g' -e 's/.out:!!//g' > scf-hse_energy.dat

grep highest scf-hse_*.out | sed -e 's/scf-hse_//g' -e 's/.out://g' > scf-hse_band.dat
