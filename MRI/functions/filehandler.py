import numpy as np
import numpy.linalg as lin
from nibabel import save, Nifti1Image
import os

from IPython.display import display

def save_nifti_image(complex_im, filename, meta_data):
    # P3
    '''
    Saves a complex valued image in nifit format in the images folder.
    
    Input:
        - complex_im  : image with complex values
        - filename    : name of the file. Must end with .nii
        - meta_data   : meta data for the image
    
    Ouput:
    '''
    assert filename.endswith(".nii"), "file ending must be .nii"
    
    if not os.path.exists('images'):
        os.makedirs('images') # if folder does not exist, create it.
        print("Created 'images' folder")
    
    abs_im = np.absolute(complex_im)

    try:
        img = Nifti1Image(abs_im, np.eye(4), extra=meta_data)
        save(img, os.path.join("images", filename))
    except:
        print("Unexpected error:", sys.exc_info()[0])
    else:
        print(f"File '{filename}' saved succesfully!")

        
def k2im(k_space):
    # A1
    '''
    Transforms k-space raw data to readable image data, slice by slice, thus assumes that the data was acquired slice by slice. 
    This is done (slice-by-slice) by first shifting the data and then inverse Fourier transform it.  
    
    Input:
        - k_space  : batch of raw data in k-space
      
    Ouptu:
        - imgs     : batch of images
    '''
    imgs = np.empty(k_space.shape, dtype='float').astype(complex)
    
    
    for i in range((k_space.shape)[2]):
        imgs[:,:,i] = np.fft.ifftshift(np.fft.ifft2(k_space[:,:,i]))
    
    return imgs
        
def SENSE(folded_ims, coil_sensitivities):
    # C2
    '''
    Combines folded images using SENSE by solving:
    
    f1(y,x) = S1(y,x)I(y,x) + S1(y+ny/2+ny/4, x) I(y+ny/2+ny/4, x)
    f2(y,x) = S2(y,x)I(y,x) + S2(y+ny/2+ny/4, x) I(y+ny/2+ny/4, x)
    
    for each pixel x,y of the folded images. 
    f1-2 is the folded images and S1-2 is the coil sensitivity images and I (=outputImages) is the image we want reconstruct. 
    ny is the size of the full FOV in the y-axis. 
    The ny/4 (=Ny4) shift is due to the folded images being in the middle of the full FOV, and also being half as large in the y-axis.  
    
    Input (compatibility unchecked):
        - folded_ims        : batch of folded images (size: nx/(ny/2)/n_imgs/2)
        - coil_sensitivites : batch of sensitivities images of the coils (size: nx/ny/n_imgs/2)
    Ouput:
        - outputImages      : batch of unfolded images (size: nx/ny/n_imgs)
    '''
    n = coil_sensitivities.shape
    Ny2 = int(n[0] / 2)
    Ny4 = int(Ny2 / 2)
    outputImages = np.empty(n[0:3], dtype='float')
    
    for img in range(n[2]): # for each image
        
        for y in range(Ny2): # top - bottom of folded images
            
            ys = [y + Ny4, (y + Ny4 + Ny2) % n[0]] # find corresponding contibutions of real signals
            
            for x in range(n[1]): # left - right
                f = folded_ims[y, x, img, :]
                S = np.transpose(coil_sensitivities[ys, x, img, :])
                
                sol,_,_,_ = lin.lstsq(S,f, rcond=-1)
                
                outputImages[ys, x, img] = sol 
    
    return outputImages

