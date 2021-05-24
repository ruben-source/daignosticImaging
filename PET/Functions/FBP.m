function F = FBP(G, theta, output_size)
    F = zeros(output_size);
    for slice = 1:output_size(3)
        F(:, :, slice) = iradon(G, theta,'Hamming', output_size(1));  
    end
end