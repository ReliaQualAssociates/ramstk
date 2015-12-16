#!/bin/sh

CLOC=`which cloc`
SED=`which sed`
MYSQL=`which mysql`
RM=`which rm`

BASEDIR="/home/andrew/projects/RTK"

INFILES="${BASEDIR}/devtools/source.files"
SQLFILE="${BASEDIR}/tests/_test_results/cloc.sql"
XMLFILE="${BASEDIR}/tests/_test_results/cloc.xml"
XSLFILE="${BASEDIR}/tests/_test_results/cloc.xsl"

SQL=0
XML=1

sql_output() {

    OPTIONS="--by-file-by-lang --list-file=${INFILES} --sql=${SQLFILE} --sql-project=RTK"

    echo " "
    echo " ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== "
    echo " Beginning CLOC run with SQL output. "
    echo " ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== "
    echo " "
    ${CLOC} ${OPTIONS}

    # Remove the SQL statement so the tables are not trying to be re-created each time 
    # and fix the syntax to be compatible with MariaDB.
    ${SED} -i '2,14d' ${SQLFILE}
    ${SED} -i 's/begin transaction/start transaction/' ${SQLFILE}

    # Update the RTK database tables with the new code counts.
    ${MYSQL} --user=andrew --host='gandolf' --password='Rudy1C@T' RTK < ${SQLFILE}

    ${RM} ${SQLFILE}

}

xml_output() {

    OPTIONS="--by-file-by-lang --list-file=${INFILES} --xsl=${XSLFILE} --xml --report-file=${XMLFILE}"

    echo " "
    echo " ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== "
    echo " Beginning CLOC run with XML output. "
    echo " ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== "
    echo " "
    ${CLOC} ${OPTIONS}

    ${SED} -i "s@${BASEDIR}/tests/_test_results/cloc.xsl@cloc.xsl@" ${XMLFILE}

}

# Get command line arguments.
while [ $# -gt 0 ];
do
	case "$1" in

        -b|--basedir)
            BASEDIR="$2"
            ;;
        -s|--sql)
            SQL=1
            XML=0
            ;;
		-x|--xml)
            SQL=0
			XML=1
			;;
	esac
	shift
done

if [ "x$SQL" == "x1" ];
then
    sql_output
fi

if [ "x$XML" == "x1" ];
then
    xml_output
fi

exit 0
