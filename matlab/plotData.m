% First test of plotting data

% load data
data = readtable('../data/Warmup_Mecatis_03_02_25/diCodeMesure.csv');

x = data.Var1;
index = 1:length(x);
y = data.Var2;

% plot
plot(index,y,'.');
xlabel('Index [-]')
ylabel('y')