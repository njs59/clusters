function [metastatic] = metastatic_invasion(n,i,N)

    cst = 0.001;
    x = 1:N;
    y = normpdf(x,60,20);
    % plot(y)
    func_mu = cst*y(i);
    metastatic = func_mu*n(i);

end