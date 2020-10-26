module Full_Adder (X1, X2, Cin, S, Cout);

input X1, X2, Cin;
output S, Cout;

wire a1, a2, a3;
reg a4;
xor u1(a1,X1,X2);
and u2(a2,X1,X2);
and u3(a3,a1,Cin);
or u4(Cout,a2,a3);
xor u5(S,a1,Cin);

endmodule