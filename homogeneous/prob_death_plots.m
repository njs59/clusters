x = 1:100;
y = geopdf(x,0.1);

figure
bar(x,y,1)
xlabel('Observation')
ylabel('Probability')

z = geopdf(100-x,0.1);

figure
bar(x,z,1)
xlabel('Observation')
ylabel('Probability')


u = y + z;

figure
bar(x,u,1)
xlabel('Observation')
ylabel('Probability')