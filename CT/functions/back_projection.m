function back_proj = back_projection(g, N)
    % back projection for all thetas, with assumed step size of 1
    back_proj = zeros(size(g, 1), size(g, 1));
    thetas = 1:ceil(size(g,1)/N):size(g,1);
    
    for theta = thetas
        back_proj = back_proj + back_projection_theta(g, theta);
    end
end