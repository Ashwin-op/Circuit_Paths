module fulladder(a,b,cin,s,cout);

input a,b,cin;
output s,cout;
wire [3:0] w, w1;
xor xor1(s,a,b,cin);
and and1(w[0],a,b);
and and2(w[1],b,cin);
and and3(w[2],a,cin);
or or1(cout,w[0],w[1],w[2]);

endmodule
