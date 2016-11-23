#!/bin/sh

pdf_dir=pdf
html_dir=html

which pdf2txt.py > /dev/null
if [ $? -ne 0 ]; then
    echo "pdf2txt.py : Not found"
    echo "> $ pip3 install --upgrade pdfminer3k"
    exit
fi

if [ ! -d $html_dir ]; then
    mkdir $html_dir
fi

for pdf in $pdf_dir/*; do
    html_file=$html_dir/`basename $pdf | sed -e 's/pdf/html/'`
    echo $html_file
    #pdf2txt.py -o $html_file $pdf 2>&1 /dev/null
    pdf2txt.py -o $html_file $pdf > /dev/null 2>&1
done

echo done

# end of file
