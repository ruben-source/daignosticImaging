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
    # TODO
    n = folded_ims.shape
    Ny = int(n[0] / 2)
    
    outputImage = np.empty(n[0:3], dtype='float')
    
    for img in range(n[2]): # for each image
        for y in range(n[0]): # for each y pos
            for x in range(n[1]): # for each x pos

                C = np.array([folded_ims[y, x, img, 0], folded_ims[y, x, img, 1]])
                S = np.array([[coil_sensitivities[y, x, img, 0], coil_sensitivities[(y + Ny) % (2*Ny - 1), x, img, 0]],
                              [coil_sensitivities[y, x, img, 1], coil_sensitivities[(y + Ny) % (2*Ny - 1), x, img, 1]]])
                
                sol,_,_,_ = np.linalg.lstsq(S,np.transpose(C), rcond=-1)
                # display(sol)
                outputImage[y, x, img] = sol[0]
                outputImage[(y + Ny) % (2*Ny - 1), x, img] = sol[1] 
    
    return outputImage