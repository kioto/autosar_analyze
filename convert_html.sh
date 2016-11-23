#!/bin/sh

pdf_dir=pdf
html_dir=html

if [ ! -d $html_dir ]; then
    mkdir $html_dir
fi

for pdf in $pdf_dir/*; do
    html_file=$html_dir/`basename $pdf | sed -e 's/pdf/html/'`
    echo $html_file
    pdf2txt.py -o $html_file $pdf >& /dev/null
done

echo done

# end of file
