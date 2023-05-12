clear all; close all; clc
x1=load("data.txt");
x2=load("data.csv");
x=x1;

figure(1);
plot(x(:,1),(X:,2),'.')
%%
figure(1);
plot(x(:,1),x(:,2),'.')
hold on;
plot(x(:,1),x(:,2),'ro')
hold off;

%%

