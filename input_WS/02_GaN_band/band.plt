unset key
set grid xtics

G1 = 0.0000
M = 0.5774
K = 0.9107
G2 = 1.5774
A = 1.8842
L = 2.4616
H = 2.7949
A2 = 3.4616
L2 = 4.0389
M2 = 4.3458
K2 = 4.6791
H2 = 4.9860

set xtics ("{/Symbol G}" G1, "{M}" M, "{K}" K, "{/Symbol G}" G2, "{A}" A, "{L}" L, "{H}" H, "{A}" A2, "{L}" L2, "{M}" M2, "{K}" K2, "{H}" H2)

set ylabel "Energy [eV]" font "Arial, 14"
set yrange [-5:9]

VBM = 9.27013 #Valence band Maximum [eV]

plot "gan.band.gnu" u 1:($2-VBM) w l lw 1.5 lc "red", \
0 w l lc "black" dt (10, 10)