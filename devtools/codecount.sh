#!/bin/sh

OUTDIR="pylintout"
OUTFILE="code.counts"
INFILES=`find relkit/ -name '*.py'`
SLOCTOT=0

rm -f $OUTDIR/*
echo '' > $OUTFILE
echo "<html><body>" > $OUTDIR/index.html
for f in $INFILES;
do
	SLOC=`pylint --rcfile=devtools/pylintrc $f | grep '|code' | cut -d '|' -f3`
	SLOCTOT=$(( SLOCTOT + SLOC ))
	echo "$f has $SLOC lines of code for a total of $SLOCTOT lines of code." >> $OUTFILE
	
	`pylint --rcfile=devtools/pylintrc --files-output=yes --output-format=html $f`
	X=`ls pylint_relkit* | cut -d '.' -f2- | sed 's/.html//'`
	mv pylint_global.html pylint_relkit.${X}_global.html
	mv -f *.html $OUTDIR

done

X=`ls $OUTDIR/ | sort | sed 's/.html//' | sed 's/pylint_relkit.//'`

for HTML in $X;
do
	if [ "${HTML}" != "index" ];
	then
		mv $OUTDIR/pylint_relkit.${HTML}.html $OUTDIR/${HTML}.html
		echo "<a href=\"${HTML}.html\">${HTML}</a><br/>" >> $OUTDIR/index.html
	fi
done

echo "</body></html>" >> $OUTDIR/index.html
