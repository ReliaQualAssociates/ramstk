#!/bin/sh

PEP8=`which pep8`
PYFLAKES=`which pyflakes`
PYLINT=`which pylint`

echo "===== ===== ===== Begin PEP8 Review ===== ===== ====="
$PEP8 --ignore=E501 $1
echo -e "===== ===== ===== End PEP8 Review ===== ===== =====\n"
echo ""

echo "===== ===== ===== Begin PYFLAKES Review ===== ===== ====="
$PYFLAKES $1
echo -e "===== ===== ===== End PYFLAKES Review ===== ===== =====\n"
echo ""

echo "===== ===== ===== Begin PYLINT Review ===== ===== ====="
$PYLINT --rcfile=/home/andrew/projects/RTK/devtools/pylintrc --msg-template='{msg_id}:{line:3d}:  {obj}: {msg} ({symbol})' --reports=n $1
echo -e "===== ===== ===== End PYLINT Review ===== ===== =====\n"

#SLOCTOT=0

#INFILES=`find rtk/ -name '*.py'`

#OUTDIR="pylintout"
#OUTFILE="code.counts"

#rm -f $OUTDIR/*
#echo '' > $OUTFILE
#echo "<html><body>" > $OUTDIR/index.html
#for f in $INFILES;
#do
#    SLOC=`$PYLINT --rcfile=devtools/pylintrc $f | grep '|code ' | cut -d '|' -f3`
#    SLOCTOT=$(( SLOCTOT + SLOC ))
#    echo "$f has $SLOC lines of code for a total of $SLOCTOT lines of code." >> $OUTFILE

#    `$PYLINT --rcfile=devtools/pylintrc --files-output=yes --output-format=html $f`
#    X=`ls pylint_rtk* | cut -d '.' -f2- | sed 's/.html//'`
#    mv pylint_global.html pylint_rtk.${X}_global.html
#    mv -f *.html $OUTDIR
#    echo -e "Analyzed file $f.\n\t\tLines of code in $f: $SLOC.\n\t\tTotal lines of code in RTK: $SLOCTOT"

#done

#X=`ls $OUTDIR/ | sort | sed 's/.html//' | sed 's/pylint_rtk.//'`

#for HTML in $X;
#do
#    if [ "${HTML}" != "index" ];
#    then
#        mv $OUTDIR/pylint_rtk.${HTML}.html $OUTDIR/${HTML}.html
#        echo "<a href=\"${HTML}.html\">${HTML}</a><br/>" >> $OUTDIR/index.html
#    fi
#done

#echo "</body></html>" >> $OUTDIR/index.html

exit 0
