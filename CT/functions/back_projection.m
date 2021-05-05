function back_proj = back_projection(g, thetas, theta_idx)
    % back projection for all thetas, with assumed step size of 1
    back_proj = zeros(size(g, 1), size(g, 1));
    
    [xs, ys] = meshgrid(-size(g, 1)/2+1:size(g, 1)/2);
    mid = floor(size(g, 1)/2) + 1; % for the indices to be right ^^ 
    
    i = 1;
    
    for theta = thetas
        
        coords = mid + floor(xs*cos(theta*pi/180) + ys*sin(theta*pi/180));
        ind = find(coords > 0 & coords <= size(g,1));
        
        back_proj(ind) = back_proj(ind) + g(coords(ind), theta_idx(i));
        i = i+1;
    end
end