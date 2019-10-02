# Module to download the dataset.

import os

import sys
if sys.version_info[0] > 2:
    from urllib.request import urlretrieve
else:
    from urllib import urlretrieve
import hashlib
import zipfile
import tarfile

def require_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return None


def download(url, target_dir, filename=None):
    require_dir(target_dir)
    if filename is None:
        filename = url_filename(url)
    filepath = os.path.join(target_dir, filename)
    urlretrieve(url, filepath)
    return filepath


def url_filename(url):
    return url.split('/')[-1].split('#')[0].split('?')[0]


def check_md5(file_name, orginal_md5):
    # Open,close, read file and calculate MD5 on its contents
    with open(file_name, 'rb') as f:
        hasher = hashlib.md5()  # Make empty hasher to update piecemeal
        while True:
            block = f.read(64 * (
                1 << 20))  # Read 64 MB at a time; big, but not memory busting
            if not block:  # Reached EOF
                break
            hasher.update(block)  # Update with new block
    md5_returned = hasher.hexdigest()
    # Finally compare original MD5 with freshly calculated
    if orginal_md5 == md5_returned:
        print('MD5 verified.')
        return True
    else:
        print('MD5 verification failed!')
        return False


def unzip(file, targetdir):
    with zipfile.ZipFile(file, "r") as zip_ref:
        zip_ref.extractall(targetdir)

def untar(file, targetdir):
    with tarfile.open(file) as tf:
        tf.extractall(targetdir)

if __name__ == '__main__':
    
    url_piano = 'http://deepyeti.ucsd.edu/cdonahue/wavegan/data/mancini_piano.tar.gz'
    md5_piano = 'd1477878bdf390cbc56cffe333a09ed1'

    print('Download Piano')
    download(url_piano, '../data/piano')
    assert(check_md5('../data/piano/mancini_piano.tar.gz', md5_piano))
    print('Extract piano dataset')
    untar('../data/piano/mancini_piano.tar.gz', '../data/')
    os.remove('../data/piano/mancini_piano.tar.gz')