## metaf-man
File manager that manages your download locations using metadata

##basics
*Create an sql database __mfm__

*Create table __meta__ with the structure below:

|Field|Type|Key|Default|Extra|
|:---|---|---|---|---|---|
|id|int(20)|NO|Pri|NULL|auto_increment|
|path|varchar(200)|YES| |NULL| |
|metadata|tinytext|YES| |NULL| |

*Run the **main.py** from inside a directory of choice (_the directory you want initialized with metadata_)

*Run the daemon using  ```python daemondummy.py  start``` and stop with ```python daemondummy.py  stop```

##todo
</ol><li>implementation using sqlite/sql automatic db creation class</li><li>Resolve ties in matching</li><li>Init script and setup</li></ol>
