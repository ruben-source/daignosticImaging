function A = compute_forward_matrix(thetas, L, R, C)
    % G = radon(F) 
    %   = A * F   {what we want find}
    %   = A * (I * F)
    %   = (A * I) * F
    %   = radon(I) * F => A = radon(I)

    % rL = size(radon(zeros(R, C), thetas(1)), 1);
    A = zeros(L*length(thetas), R*C);
    
    for i = 1:length(thetas)
        idx = 1 + (i-1)*L:i*L; 
        for j = 1:R*C
            I = zeros(R, C); I(j) = 1; % only one base
            rad = radon(I, thetas(i));
            A(idx,j) = rad(floor((end/2-L/2+1):(end/2+L/2)));
            % error("stop")
        end
    end

end