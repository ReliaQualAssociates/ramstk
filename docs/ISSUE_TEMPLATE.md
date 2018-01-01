### Expected Behavior ###

### Actual Behavior ###

### Steps to Reproduce the Problem ###

### Operating Environment ###

* Operating System:
* OS Distribution (if Linux):
* OS Version:
* Hardware:
* Required Software Versions:
  * Python ==
  * defusedxml ==
  * lifelines ==
  * lxml ==
  * matplotlib ==
  * numpy ==
  * pandas ==
  * pypubsub ==
  * scipy ==
  * sortedcontainers ==
  * sqlalchemy ==
  * sqlalchemy_utils ==
  * statsmodels ==
  * treelib ==
  * xlrd ==
  * xlwt ==

Execute something such as the following to get the required run-time package
versions for the list above.  You will need a copy of the requirements.txt file
in the repository.

    `for file in $(cat requirements.txt | cut -d '=' -f1);
        do version=$(pip show $file | grep Version: | cut -d ':' -f2-);
        echo $file ==$version;
     done`
