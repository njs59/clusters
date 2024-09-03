function model = Smol_5()


    % Symbolic variables
    syms x1 x2 x3 x4 x5
    syms b p N

    % Parameters
    model.sym.p = [b;p;N];

    % State variables
    model.sym.x = [x1;x2;x3;x4;x5];

    % Control vectors (g)
    model.sym.g=[];

    % Autonomous dynamics (f)
    model.sym.xdot=[-b*x1*(x1+x2+x3+x4) - p*x1
                 -b*x2*(x1+x2+x3) + (b/2)*x1*x1 + p*x1 - p*x2
                 -b*x3*(x1+x2) + (b)*x1*x2 + p*x3 - p*x3
                 -b*x4*(x1) + (b)*x1*x3 + (b/2)*x2*x2 + p*x3 - p*x4
                 b*x1*x4 + b*x2*x3 + p*x4];   

    % Initial conditions
    model.sym.x0 = [N;0;0;0;0];

    % Observables
    model.sym.y = [x1;x2;x3;x4;x5];
end