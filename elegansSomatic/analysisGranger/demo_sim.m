%clear all;

%  activity=table2array(Activity);
%  activity=logical(activity);
%  X=activity;

% Load simulated data
% load data_sim_9neuron.mat;     % 9-neuron network
% load data_sim_hidden.mat;      % 5-neuron network with hidden feedback
load data_elegans_compose.mat

% Dimension of input data (L: length, N: number of neurons)
[L,N] = size(X);

% To fit GLM models with different history orders
for neuron = 1:N                            % neuron
    for ht = 2:2:10                         % history, when W=2ms
        [bhat{ht,neuron}] = glmwin(X,neuron,ht,200,2);
    end
end

% To select a model order, calculate AIC
for neuron = 1:N
    for ht = 2:2:10
        LLK(ht,neuron) = log_likelihood_win(bhat{ht,neuron},X,ht,neuron,2); % Log-likelihood
        aic(ht,neuron) = -2*LLK(ht,neuron) + 2*(N*ht/2 + 1);                % AIC
    end
end

% % To plot AIC 
% round(sqrt(N)+0.5)
% 
% figure(neuron);
% for neuron = 1:N
%     subplot(5,7,neuron)
%     plot(aic(2:2:10,neuron));
% end

% Save results
%save('result_sim','bhat','aic','LLK');
save('ResModels','bhat','aic','LLK')

% Identify Granger causality
%CausalTest;