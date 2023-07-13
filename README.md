# 0x00. AirBnB clone - The console

## Project description
The console is a command-line interface(CLI) that mimics the basic fuctionality of the AirBnB website. It allows users to interact with the application and perform various operations such as creating a new object(eg: a new User or a new Place), Retrieve an object from a file or a database etc…, Do operations on objects (count, compute stats, etc…), Update attributes of an object and Destroy an object.

## Command Interpreter Dscription
The command Interpreter is a Python-based interactive shell that provides a command-line interface to interact with the AirBnB application. It allows users to execute various command to manipulate and manage objects within the application's data storage(Using the json module)

## How to start it
1. Open a terminal or command prompt.
2. Navigate to the directory where the AirBnB clone is. ```git clone https://github.com/Ekekwecharles/AirBnB_clone.git```
3. Run the `console.py` file
```./console.py```
4. The console will start, displaying a prompt `(hbnb)`. You are now reaedy to enter commands and interact with the AirBnB application.

## How to use it
Works both in Interactive and Non-interactive mode
### Some of the commands
- `create`: Create a new object.
- `show`: Display details of a specific object.
- `count`: Counts the objects
- `update`: Update properties of an object
- `destroy`: Delete an object.

## Examples
### Interactive mode:
```
$ ./console.py
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  help  quit

(hbnb) 
(hbnb) 
(hbnb) quit
$
```

### Non-interactive mode:
```
$ echo "help" | ./console.py
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb) 
$
$ cat test_help
help
$
$ cat test_help | ./console.py
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb) 
$ 
```
