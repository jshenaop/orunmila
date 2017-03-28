import os
import sys
import re
import time
import math
import urllib
import urllib2
import tarfile


def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def connect_earthexplorer_no_proxy():
    # mkmitchel (https://github.com/mkmitchell) solved the token issue
    cookies = urllib2.HTTPCookieProcessor()
    opener = urllib2.build_opener(cookies)
    urllib2.install_opener(opener)

    data = urllib2.urlopen("https://ers.cr.usgs.gov").read()
    m = re.search(r'<input .*?name="csrf_token".*?value="(.*?)"', data)
    if m:
        token = m.group(1)
    else:
        print "Error : CSRF_Token not found"
        sys.exit(-3)

    params = urllib.urlencode(dict(username='jshenaop', password='Neuralnet1985', csrf_token=token))
    request = urllib2.Request("https://ers.cr.usgs.gov/login", params, headers={})
    f = urllib2.urlopen(request)

    data = f.read()
    f.close()
    if data.find('You must sign in as a registered user to download data or place orders for USGS EROS products') > 0:
        print "Authentification failed"
        sys.exit(-1)
    return


def download_chunks(url, rep, nom_fic):
    """ Downloads large files in pieces
     inspired by http://josh.gourneau.com
    """
    try:
        req = urllib2.urlopen(url)
        # if downloaded file is html
        if (req.info().gettype() == 'text/html'):
            print "error : file is in html and not an expected binary file"
            lines = req.read()
            if lines.find('Download Not Found') > 0:
                raise TypeError
            else:
                with open("error_output.html", "w") as f:
                    f.write(lines)
                    print "result saved in ./error_output.html"
                    sys.exit(-1)
        # if file too small
        total_size = int(req.info().getheader('Content-Length').strip())
        if (total_size < 50000):
            print "Error: The file is too small to be a Landsat Image"
            print url
            sys.exit(-1)
        print nom_fic, total_size
        total_size_fmt = sizeof_fmt(total_size)

        # download
        downloaded = 0
        CHUNK = 1024 * 1024 * 8
        with open(rep + '/' + nom_fic, 'wb') as fp:
            start = time.clock()
            print('Downloading {0} ({1}):'.format(nom_fic, total_size_fmt))
            while True:
                chunk = req.read(CHUNK)
                downloaded += len(chunk)
                done = int(50 * downloaded / total_size)
                sys.stdout.write('\r[{1}{2}]{0:3.0f}% {3}ps'
                                 .format(math.floor((float(downloaded)
                                                     / total_size) * 100),
                                         '=' * done,
                                         ' ' * (50 - done),
                                         sizeof_fmt((downloaded // (time.clock() - start)) / 8)))
                sys.stdout.flush()
                if not chunk: break
                fp.write(chunk)
    except urllib2.HTTPError, e:
        if e.code == 500:
            pass  # File doesn't exist
        else:
            print "HTTP Error:", e.code, url
        return False
    except urllib2.URLError, e:
        print "URL Error:", e.reason, url
        return False

    return rep, nom_fic


def download(scene_repository, scene):
    url = 'https://earthexplorer.usgs.gov/download/4923/{}/STANDARD/EE'.format(scene)
    path_row = scene[3:9]
    rep = '{}/{}'.format(scene_repository, path_row)
    nom_fic = '{}.tar.gz'.format(scene)
    download_chunks(url, rep, nom_fic)


def prepare_dir(scene_repository, path, row):
    dir = path+row
    if not os.path.exists("{}/{}".format(scene_repository, dir)):
        os.makedirs("{}/{}".format(scene_repository, dir))


def uncompress(scene_repository, path, row, scene):

    if not os.path.exists(scene_repository + '/' + (path+row) + '/' + scene):
        os.makedirs(scene_repository + '/' + (path+row) + '/' + scene)
    else:
        pass

    file = scene_repository + '/' + (path+row) + '/' + scene + '.tar.gz'
    tar = tarfile.open(file)
    tar.extractall(path=scene_repository + '/' + (path+row) + '/' + scene)
    tar.close()


def main():
    pass

if __name__ == '__main__':
    main()
