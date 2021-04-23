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
    Ny2 = int(n[0] / 2)
    Ny4 = int(Ny2 / 2)
    outputImages = np.empty(n[0:3], dtype='float')
    
    for img in range(n[2]): # for each image
        
        for y in range(Ny2): # top - bottom of folded images
            ys = [y + Ny4, (y + Ny4 + Ny2) % n[0]]
            
            for x in range(n[1]): # left - right
                f = folded_ims[y, x, img, :]
                S = np.transpose(coil_sensitivities[ys, x, img, :])
                
                sol,_,_,_ = lin.lstsq(S,f, rcond=-1)
                
                outputImages[ys, x, img] = sol 
    
    return outputImages

'''
f1(x,y) = S1(x,y)I(x,y) + S1(x,y+ny/2)I(x,y+ny/2)
And
f2(x,y) = S2(x,y)I(x,y) + S2(x,y+ny/2)I(x,y+ny/2)
for each pixels.
Where f1-2 is the folded images and S1-2 is the coil sensitivity images and I is the image we want reconstruct. 
'''