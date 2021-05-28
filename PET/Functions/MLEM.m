function [F, r_error] = MLEM(A, G, output_size, nbr_iter)
    % Get initial guess with naive solver?
    F = zeros(output_size);
    r_error = zeros(nbr_iter+1, 1);
    
    % used for updating expression
    div = sum(A)';
    
    f = ones(size(A, 2), output_size(3));
    
    for k = 1:nbr_iter
        
        for slice = 1:output_size(3)
             
            g = G(:,:,slice);
            % g_hat_i = sum_j(a_ij*f_j)
            g_hat = A * f(:, slice);
            r_error(k) = sumsqr(g_hat - g(:));
           
            % f = f / sum_i(a_ij) * sum_i(a_ij * g_i / g_hat_i)
            f(: , slice) = f(:, slice)./div .* (A'*(g(:)./g_hat));
        end
    end
    
    % calculate last error and reshape f to F
    for slice = 1:output_size(3)
        g = G(:,:,slice);
        r_error(nbr_iter+1) = r_error(nbr_iter+1) + ...
                                sumsqr(A*f(:, slice) - g(:));
        
        F(:,:,slice) = reshape(f(:, slice), output_size(1:2));
    end
end