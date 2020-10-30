module fulladder(a,b,cin,s,cout);

input a,b,cin;
output s,cout;
wire w1,w2,w3;
xor xor1(s,a,b,cin);
and and1(w1,a,b);
and and2(w2,b,cin);
and and3(w3,a,cin);
or or1(cout,w1,w2,w3);

endmodule
