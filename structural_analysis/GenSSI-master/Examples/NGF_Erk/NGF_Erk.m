function model = NGF_Erk()
    % NGF_Erk provides the GenSSI implementation of the transformed 5-state
    % model of NFG-induced Erk signalling described in
    % 
    %    Hasenauer et al. (2014). ODE constrained mixture modelling:
    %    a method for unraveling subpopulation structures and dynamics, 
    %    PLoS Computational Biology, 10, e1003686.
    %
    % The model is transformed to remove some of the structural
    % non-identifiability. It is however still non-identifiable.
    % The initial conditions are chosen such that the model is in steady
    % state for NGF_0 = 0.

    % Symbolic variables
    syms k_1 k_2 k_4 k_5 k_7 k_9 k_11
    syms k_3__TrkA_NGF k_6__RasGTP k_8__pRaf k_10__pMek s__pErk
    syms k_3__TrkA_0 k_6__Ras_0 k_8__Raf_0 k_10__Mek_0 s__Erk_0 s_K n NGF_0

    % Parameters
    model.sym.p = [k_1;k_2;k_4;k_5;k_7;k_9;k_11;...
                   k_3__TrkA_0;k_6__Ras_0;k_8__Raf_0;k_10__Mek_0;...
                   s__Erk_0;s_K;n;NGF_0];
	
    % State variables
    model.sym.x = [k_3__TrkA_NGF
                   k_6__RasGTP
                   k_8__pRaf
                   k_10__pMek
                   s__pErk];

    % Control vectors (g)
    model.sym.g = [];
	
    % Autonomous dynamics (f)
    model.sym.xdot = [-k_3__TrkA_NGF*k_2-NGF_0*k_1*(k_3__TrkA_NGF-k_3__TrkA_0)
                      -k_6__RasGTP*k_5-(k_6__RasGTP-k_6__Ras_0)*(k_4+(k_3__TrkA_NGF*s_K^n)/(s__pErk^n+s_K^n))
                       k_6__RasGTP*(k_8__Raf_0-k_8__pRaf)-k_7*k_8__pRaf
                       k_8__pRaf*(k_10__Mek_0-k_10__pMek)-k_9*k_10__pMek
                      -k_11*s__pErk-k_10__pMek*(s__pErk-s__Erk_0)];

    % Initial conditions
	model.sym.x0 = [0
                    (k_4*k_6__Ras_0)/(k_4 + k_5)
                    (k_4*k_6__Ras_0*k_8__Raf_0)/((k_4 + k_5)*(k_7 + (k_4*k_6__Ras_0)/(k_4 + k_5)))
                    (k_4*k_6__Ras_0*k_8__Raf_0*k_10__Mek_0)/((k_4 + k_5)*(k_7 + (k_4*k_6__Ras_0)/(k_4 + k_5))*(k_9 + (k_4*k_6__Ras_0*k_8__Raf_0)/((k_4 + k_5)*(k_7 + (k_4*k_6__Ras_0)/(k_4 + k_5)))))
                    (k_4*k_6__Ras_0*k_8__Raf_0*k_10__Mek_0*s__Erk_0)/((k_4 + k_5)*(k_7 + (k_4*k_6__Ras_0)/(k_4 + k_5))*(k_11 + (k_4*k_6__Ras_0*k_8__Raf_0*k_10__Mek_0)/((k_4 + k_5)*(k_7 + (k_4*k_6__Ras_0)/(k_4 + k_5))*(k_9 + (k_4*k_6__Ras_0*k_8__Raf_0)/((k_4 + k_5)*(k_7 + (k_4*k_6__Ras_0)/(k_4 + k_5))))))*(k_9 + (k_4*k_6__Ras_0*k_8__Raf_0)/((k_4 + k_5)*(k_7 + (k_4*k_6__Ras_0)/(k_4 + k_5)))))];

    % Observables
	model.sym.y = [s__pErk];
end
