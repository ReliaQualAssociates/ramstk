#!/bin/sh

PYLINT=`which pylint`

SLOCTOT=0

INFILES=`find rtk/ -name '*.py'`

OUTDIR="pylintout"
OUTFILE="code.counts"

rm -f $OUTDIR/*
echo '' > $OUTFILE
echo "<html><body>" > $OUTDIR/index.html
for f in $INFILES;
do
	SLOC=`$PYLINT --rcfile=devtools/pylintrc $f | grep '|code ' | cut -d '|' -f3`
	SLOCTOT=$(( SLOCTOT + SLOC ))
	echo "$f has $SLOC lines of code for a total of $SLOCTOT lines of code." >> $OUTFILE

	`$PYLINT --rcfile=devtools/pylintrc --files-output=yes --output-format=html $f`
	X=`ls pylint_rtk* | cut -d '.' -f2- | sed 's/.html//'`
	mv pylint_global.html pylint_rtk.${X}_global.html
	mv -f *.html $OUTDIR
	echo -e "Analyzed file $f.\n\t\tLines of code in $f: $SLOC.\n\t\tTotal lines of code in RTK: $SLOCTOT"

done

X=`ls $OUTDIR/ | sort | sed 's/.html//' | sed 's/pylint_rtk.//'`

for HTML in $X;
do
	if [ "${HTML}" != "index" ];
	then
		mv $OUTDIR/pylint_rtk.${HTML}.html $OUTDIR/${HTML}.html
		echo "<a href=\"${HTML}.html\">${HTML}</a><br/>" >> $OUTDIR/index.html
	fi
done

echo "</body></html>" >> $OUTDIR/index.html
