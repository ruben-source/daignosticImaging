% Convolutional Backprojection with filtering (+Hamming in B3)

function FBPI = conv_back_projection(sinogram, thetas, idx, filter)
    [gl, nt] = size(sinogram); % Get size of l component of sinogram
    mid = floor(gl / 2);    % Set the midpoint
    
    % Need to generate ramp high pass filter in one period in the
    % positive frequency domain
    if mod(gl, 2) == 0
        ramp = [0:mid, mid-1:-1:1];
    else
        ramp = [0:mid, mid-1:-1:0];
    end
    % - Filter function H
    % Add hamming here for B3, maybe switch case? Currently string input
    
    if nargin < 4
        filter = 'hamming'; % set hamming as default
    end
    
    if filter == "ramp"
        H = ramp';
    elseif filter == "hamming"
        h = hamming(size(sinogram, 1));
        H = [h(mid:gl); h(1:mid-1)].*ramp';
    else
        fprintf('Incorrect filter input. Should be ramp or hamming.')
    end
    
   % Fourier transform sinogram data: g(l, theta) -> g(w, theta)
   c = real(ifftshift(ifft(H)));
   
   % Multiply with filter, element wise multiplication
   g_filtered = convn(sinogram, c, 'same');
   
   % Use backprojection to generate the filtered image
   FBPI = back_projection(g_filtered,thetas, idx);
end
    
    