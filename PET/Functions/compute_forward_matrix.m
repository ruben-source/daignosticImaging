function A = compute_forward_matrix(thetas, L, R, C)
    % rL = size(radon(zeros(R, C), thetas(1)), 1);
    A = zeros(L*length(thetas), R*C);
    
    for i = 1:length(thetas)
        idx = 1 + (i-1)*L:i*L; 
        for j = 1:R*C
            I = zeros(R, C); I(j) = 1; % only one base
            rad = radon(I, thetas(i));
            A(idx, j) = rad(1:L);
        end
    end

end