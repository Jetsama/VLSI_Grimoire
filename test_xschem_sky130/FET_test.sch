v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 1590 -1040 1670 -1040 {
lab=#net1}
N 1590 -980 1710 -980 {
lab=#net2}
N 1710 -1010 1710 -980 {
lab=#net2}
N 1710 -1090 1710 -1070 {
lab=#net3}
N 1710 -1090 1830 -1090 {
lab=#net3}
N 1830 -1090 1830 -1070 {
lab=#net3}
N 1830 -1010 1830 -980 {
lab=#net2}
N 1710 -980 1830 -980 {
lab=#net2}
C {sky130_fd_pr/nfet3_01v8.sym} 1690 -1040 0 0 {name=M1
W=1
L=0.15
body=GND
nf=1
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {vsource.sym} 1590 -1010 0 0 {name=V1 value=3 savecurrent=false}
C {vsource.sym} 1830 -1040 0 0 {name=V3 value=3 savecurrent=false}
