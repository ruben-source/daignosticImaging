function [F, r_error] = MLEM(A, G, output_size, nbr_iter)
    % Get initial guess with naive solver?
    F = NAIVE(A, G, output_size);
    r_error = zeros(nbr_iter+1, 1);
    
    for k = 1:nbr_iter
        % Probably incorrect, we're basing this off eq 9.35
        r_error(k) = A*F - G;
        for slice = 1:output_size(3)
            % Eq. 9.34
            F(:,:, slice) = F(:,:,slice) - (r_error(k)/(A*A))*A;
        end
    end
    r_error(nbr_iter+1) = A*F - G; % What should the final value of r_error be?
end