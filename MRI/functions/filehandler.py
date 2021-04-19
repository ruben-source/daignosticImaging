import numpy as np
import numpy.linalg as lin
from nibabel import save, Nifti1Image
from os.path import join

from IPython.display import display

def save_nifti_image(complex_im, filename, meta_data):
    # P3
    abs_im = np.absolute(complex_im)

    try:
        img = Nifti1Image(abs_im, np.eye(4), extra=meta_data)
        save(img, join("images", filename))
    except:
        print("Unexpected error:", sys.exc_info()[0])
    else:
        print(f"File {filename} saved succesfully!")

        
def k2im(k_space):
    # A1
    img = np.empty(k_space.shape, dtype='float').astype(complex)
    
    # Assume that the data was acquired slice by slice
    
    for i in range((k_space.shape)[2]):
        img[:,:,i] = np.fft.ifftshift(np.fft.ifft2(k_space[:,:,i]))
    
    return img
        
def SENSE(folded_ims, coil_sensitivities):
    
    n = coil_sensitivities.shape
    Ny = int(n[0] / 2)
    
    outputImage = np.empty(n[0:3], dtype='float')
    
    for img in range(n[2]): # for each image
        for x in range(n[1]): # left - right
            for y in range(Ny): # top - bottom
                C = folded_ims[y, x, img, :]
                S = coil_sensitivities[[y, (y + Ny) % (n[0] - 1)], x, img, :]
                
                
                sol,_,_,_ = lin.lstsq(S,C, rcond=-1)
                
                outputImage[[y, (y + Ny) % (n[0] - 1)], x, img] = sol 
    
    return outputImage

'''
S1(x,y) = C1(x,y)I(x,y) + C2(x,y+ny/2)I(x,y+ny/2)
And
S2(x,y) = C1(x,y)I(x,y) + C1(x,y+ny/2)I(x,y+ny/2)
for each pixels.
Where S1-2 is the signal images (folded) and C1-2 is the coil images and I is the image we want reconstruct. 
'''