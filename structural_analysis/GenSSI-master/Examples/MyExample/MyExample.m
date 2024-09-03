function model = MyExample()


    % Symbolic variables
    syms x1 x2 x3 x4 x5
    % syms x1 x2 x3 x4 x5 x6 x7 x8 x9 x10
    syms b p N
    % syms b11 b12 b13 b14 b22 b23 p1 p2 p3 p4 N

    % Parameters
    % model.sym.p = [b11;b12;b13;b14;b22;b23;p1;p2;p3;p4;N];
    model.sym.p = [b;p;N];

    % State variables
    model.sym.x = [x1;x2;x3;x4;x5];
    % model.sym.x = [x1;x2;x3;x4;x5;x6;x7;x8;x9;x10];

    % Control vectors (g)
    model.sym.g=[];

    % Autonomous dynamics (f)
    % model.sym.xdot=[-x1*(b11*x1+b12*x2+b13*x3+b14*x4) - p1*x1
    %              -x2*(b12*x1+b22*x2+b23*x3) + (b11/2)*x1*x1 + p1*x1 - p2*x2
    %              -x3*(b13*x1+b23*x2) + (b12)*x1*x2 + p2*x2 - p3*x3
    %              -x4*(b14*x1) + (b13)*x1*x3 + (b22/2)*x2*x2 + p3*x3 - p4*x4
    %              b14*x1*x4 + b23*x2*x3 + p4*x4];
        % Autonomous dynamics (f)
%% GENERAL EQN HERE
    model.sym.xdot=[-b*x1*(x1+x2+x3+x4) - p*x1
                 -b*x2*(x1+x2+x3) + (b/2)*x1*x1 + p*x1 - p*x2
                 -b*x3*(x1+x2) + (b)*x1*x2 + p*x2 - p*x3
                 -b*x4*(x1) + (b)*x1*x3 + (b/2)*x2*x2 + p*x3 - p*x4
                 b*x1*x4 + b*x2*x3 + p*x4];
%% Max = 10
    % model.sym.xdot=[-b*x1*(x1+x2+x3+x4+x5+x6+x7+x8+x9) - p*x1
    %              -b*x2*(x1+x2+x3+x4+x5+x6+x7+x8) + (b/2)*x1*x1 + p*x1 - p*x2
    %              -b*x3*(x1+x2+x3+x4+x5+x6+x7) + (b)*x1*x2 + p*x2 - p*x3
    %              -b*x4*(x1+x2+x3+x4+x5+x6) + (b)*x1*x3 + (b/2)*x2*x2 + p*x3 - p*x4
    %              -b*x5*(x1+x2+x3+x4+x5) + b*x1*x4 + b*x2*x3 + p*x4 - p*x5
    %              -b*x6*(x1+x2+x3+x4) + b*x1*x5 + b*x2*x4 + (b/2)*x3*x3 + p*x5 - p*x6
    %              -b*x7*(x1+x2+x3) + b*x1*x6 + b*x2*x5 + b*x3*x4 + p*x6 - p*x7
    %              -b*x8*(x1+x2) + b*x1*x7 + b*x2*x6 + b*x3*x5 + (b/2)*x4*x4 + p*x7 - p*x8
    %              -b*x9*(x1) + b*x1*x8 + b*x2*x7 + b*x3*x6 + b*x4*x5 + p*x8 - p*x9
    %              b*x1*x9 + b*x2*x8 + b*x3*x7 + b*x4*x6 + (b/2)*x5*x5 + p*x9];


    % Initial conditions
    model.sym.x0 = [N;0;0;0;0];
    % model.sym.x0 = [N;0;0;0;0;0;0;0;0;0];

    % Observables
    model.sym.y = [x1;x2;x3;x4;x5];
    % model.sym.y = [x1;x2;x3;x4;x5;x6;x7;x8;x9;x10];
end