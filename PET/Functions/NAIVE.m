function F = NAIVE(A, G, output_size)
    F = zeros(output_size);
    for slice = 1:output_size(3)
        g = G(:,:, slice);
        f = A \ g(:);
        F(:, :, slice) = reshape(f, output_size(1:2));           
    end
end