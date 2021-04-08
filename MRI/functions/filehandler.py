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
        
def test_func():
    print("some stuff")