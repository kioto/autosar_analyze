#-*- utf-8 -*-

import os
import os.path
import sys
import re
import urllib.request
import html.parser as hp

class ArParser(hp.HTMLParser):
    def __init__(self):
        hp.HTMLParser.__init__(self)
        self.links = []
        self.url = ''
        self.text = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            attrs = dict(attrs)
            if 'href' in attrs:
                self.url = attrs['href']

    def handle_endtag(self, tag):
        if tag == 'a':
            if self.text:
                self.links.append((self.url, self.text))
            self.url = ''
            self.text = ''

    def handle_data(self, data):
        if self.url:
            self.text += data

def download_file(url, outdir):
    url_obj = urllib.request.urlopen(url)
    filename = os.path.join(outdir, os.path.basename(url))
    pdf = open(filename, 'wb')
    pdf.write(url_obj.read())
    url_obj.close()
    pdf.close()

def get_pdfurl(url):
    pdf_list = []
    urlp = urllib.parse.urlparse(url)
    url_top = urlp.scheme+'://'+urlp.netloc+'/'
    with urllib.request.urlopen(url) as response:
        parser = ArParser()
        parser.feed(response.read().decode('utf-8'))
        response.close()
        for (link, text) in parser.links:
            if link.endswith('.pdf'):
                if not link.startswith('http'):
                    link = url_top+link
                pdf_list.append(link)
    return pdf_list

def print_usage():
    print('Usage: %s <urlfile> <outdir>' % sys.argv[0])


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print_usage()
        exit()
    urlfile = sys.argv[1]
    outdir = sys.argv[2]

    try:
        f = open(urlfile)
        if not os.path.exists(outdir):
            os.mkdir(outdir)
        for line in f.readlines():
            line = line.rstrip()
            if not line or line.startswith('#'):
                continue
            line = line.rstrip()
            print("[URL: %s]" % line)
            pdfurl_list = get_pdfurl(line)
            for pdfurl in pdfurl_list:
                download_file(pdfurl, outdir)
                print('download %s' % os.path.basename(pdfurl))
        f.close()
        print('done')
    except IOError:
        pass
    except OSError:
        pass


# end of file
