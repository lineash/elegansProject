% Preparing connectivity analysis data to export to R
% and analize there.

load dataPharynx.mat

% Dimension of input data (L: length, N: number of neurons)
[L,N] = size(X);

% Create a cell array to add Phi connections
fConn={'from', 'to', 'connPhi', 'connPsi1', 'connPsi2'};

%%% Import names manually as a cell array called names with two 
%%% rows, first for 'n1', 'n2', etc.; second for cell names.

for trigger = 1:N
    for target=1:N
        fConn{(trigger-1)*N+target,1}=names{2,trigger};
        fConn{(trigger-1)*N+target,2}=names{2,target};
        fConn{(trigger-1)*N+target,3}=Phi(target,trigger);
        fConn{(trigger-1)*N+target,4}=Psi1(target,trigger);
        fConn{(trigger-1)*N+target,5}=Psi2(target,trigger);
    end
end
    
colnames = {'from', 'to', 'connPhi', 'connPsi1', 'connPsi2'};
fConn=cell2table(fConn,'VariableNames',colnames);

writetable(fConn,'fConn.csv')


