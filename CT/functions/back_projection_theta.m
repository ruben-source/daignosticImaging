function back_proj = back_projection_theta(g, theta)
    % back projection for a given theta
    back_proj = zeros(size(g,1), size(g, 1));

    % xs = -size(g, 1)/2+1:size(g, 1)/2;
    % ys = xs;
    [xs, ys] = meshgrid(-size(g, 1)/2+1:size(g, 1)/2);
    
    mid = floor(size(g, 1)/2) + 1; % for the indices to be right ^^ 

    coords = mid + floor(xs*cos(theta*pi/180) + ys*sin(theta*pi/180));
    ind = find(coords > 0 & coords <= size(g,1));
    back_proj(ind) = g(coords(ind), theta);
end