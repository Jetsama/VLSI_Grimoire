v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N -0 -190 -0 -160 {
lab=VDD}
N 0 -70 0 -40 {
lab=VSS}
N -60 -160 -40 -160 {
lab=IN}
N -60 -160 -60 -70 {
lab=IN}
N 0 -130 -0 -100 {
lab=IN}
N -120 -120 -60 -120 {
lab=IN}
N 0 -40 -0 -20 {
lab=VSS}
N -20 -20 0 -20 {
lab=VSS}
N -40 -230 0 -230 {
lab=VDD}
N 0 -230 0 -190 {
lab=VDD}
N -60 -70 -40 -70 {
lab=IN}
N 0 -120 90 -120 {
lab=IN}
C {/foss/pdks/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} -20 -70 0 0 {name=M1
L=0.15
W=1
nf=1 
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {/foss/pdks/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} -20 -160 0 0 {name=M2
L=0.15
W=1
nf=1
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {iopin.sym} -120 -120 0 1 {name=p1 lab=IN
}
C {iopin.sym} -40 -230 0 1 {name=p5 lab=VDD
}
C {iopin.sym} -20 -20 0 1 {name=p6 lab=VSS
}
C {iopin.sym} 90 -120 0 0 {name=p7 lab=IN
}
C {code.sym} -270 -110 0 0 {name=spice only_toplevel=false value="
.lib /foss/pdks/sky130A/libs.tech/ngspice/sky130.lib.spice tt

"}
