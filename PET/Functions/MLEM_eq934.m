function [F, r_error] = MLEM(A, G, output_size, nbr_iter)
    % Get initial guess with naive solver?
    F = zeros(output_size);
    r_error = zeros(nbr_iter+1, 1);
    
    % used for updating expression
    div = (1 ./ diag(A * A')) .* A;
    
    f = ones(size(A, 2), output_size(3));    
    for k = 1:nbr_iter
        
        for slice = 1:output_size(3)
            
            g = G(:,:,slice);
            residual = A*f(:, slice) - g(:);
            
            r_error(k) = r_error(k) + sumsqr(residual);
            
            % Eq. 9.34
            % f_k = f_k-1 - (a_i*f_k-1 - g_i) / (a_i * a_i) * a_i
            f(:, slice) = f(:,slice) - sum(residual .* div)';
                        
        end
    end
    
    % calculate last error and reshape f to F
    for slice = 1:output_size(3)
        g = G(:,:,slice);
        r_error(nbr_iter+1) = r_error(nbr_iter+1) + sumsqr(A*f(:, slice) - g(:));
        
        F(:,:,slice) = reshape(f(:, slice), output_size(1:2));
    end
end