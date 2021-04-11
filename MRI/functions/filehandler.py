import numpy as np
from nibabel import save, Nifti1Image
from os.path import join

def save_nifti_image(complex_im, filename, meta_data):
    abs_im = np.absolute(complex_im)

    try:
        img = Nifti1Image(abs_im, np.eye(4), extra=meta_data)
        save(img, join("images", filename))
    except:
        print("Unexpected error:", sys.exc_info()[0])
    else:
        print(f"File {filename} saved succesfully!")

        
def k2im(k_space):
    img = np.empty(k_space.shape, dtype='float').astype(complex)
    
    for i in range((k_space.shape)[2]):
        img[:,:,i] = np.fft.ifftshift(np.fft.ifft2(k_space[:,:,i]))

    # img = np.fft.ifftshift(np.fft.ifftn(k_space))
    
    return img
        
def test_func():
    print("some stuff")