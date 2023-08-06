# Min - Binary Heap Implementation
PYPI module that provides Min, Binary Heap, functionality.

#Overview
Documentation for the Min - Binary Heap Implementation:
# 0. Preliminary Information

     Upon Creating a memmap with the build_heap function, a directory that will hold the memmap files
     will be created. After the build_heap function is finished, an information list will be returned containing
     the following elements in order: 1. memmap list, 2. # of Levels, 3. Max Occupied Index value, 4. # of Nodes, 5. Data File reference.
     The Developer should not mess with any of these information list elements. Should the developer accidentally tamper with the list values,
     there is a recalibration function that will restore the information list; this assumes that the developer does not mess with the
     files within the created directory. Should the Data file or any other file be erased, the recalibration function will no longer work,
     and the developer should start over with creating a heap.

     Additionally, since the heap elements are stored in files, the developer can add any elements he/she wants and continue on the next day
     by using the recalibration function to restore the information list.

# 1. Core Functions:

  How to use: <br/>
      from MinHeap import FUNCTION_NAME or from MinHeap import *

  ## def createBTO()
      +Creates a memmap matrix of shape:1000 x 1000 and returns an INFO list
       containing the following: [memmap list, # of Levels, Largest Index, Number of Nodes, Data File]

  ## def getHeightThree(INFO, value)
     +Returns the height of a certain value within the tree or None if it can't be found...
     	      +INFO = information list
	      	      +value = the node value that will be searched for...

  ## def reCalibrateInfo()
     +This function only requires that the user be within the binary tree directory initially created; if not -1 is returned.
      -1 is also returned if all of the files within are deleted...
     	   + No arguments required...

  ## def isFullTree(INFO)
     +Returns 1 if the tree is a full tree where each node has either zero or two children; -1 if not...
     	      +INFO = information list

  ## def isPerfect(INFO)
     +Returns 1 if the tree is a perfect tree or -1 if not...

  ## def BreadthFirstOne(INFO, value)
     +This function uses the breadth first search algorithm to find a specified node value. Three non-negative values will
      be returned if the search is successful: x = memmap list component, y = row, z = column -> Or -1, -1, -1 if unseccussful.
     	   +INFO = information list
	   	   +value = node value to be searched for...

  ## def getMinValue(INFO)
     +returns the min value or None if no values are present.
     	      +INFO = information list

  ## def ExtractMinValue(INFO)
     +Retruns the min value and deletes it from the tree or returns None if no values are present.
     	      +INFO = information list

  ## def AddValue(INFO, Value)
     +Adds a value to the tree and re-organizes accordingly; returns None if unsuccessful or "Value" if successful.
     	   +INFO = information list
	   	   +Value = The value to be added (of type float or int)...

# Example1:

	A = createBTO() # A is the information list

	#add a value
	result = AddValue(A, 100) # 100 returned since adding was successful

	#extract a value...
	value = ExtractMinValue(A)

	#add a value
	result = AddValue(A, 'B') # None returned since 'B' is not of type int or float
	result = AddValue(A, 100.56) # 100.56 returned since adding was successful
	result = AddValue(A, -900) # -900 returned since adding was successful
	result = AddValue(A, -800) # -800 returned since adding was successful

	#get min value...
	value = getMinValue(A) # -900 is returnd

	#see if it is a full tree...
	full = isFullTree(A)

	#add a value
	result = AddValue(A, 9000)
	result = AddValue(A, -67)
	result = AddValue(A, -39)

	#perform a breadth first search...
	a, b, c = BreadthFirstOne(A, 3000) # will return -1, -1, -1 since 3000 was not added...

# Example2:

	Say we have the structure from example 1. We have several values: 9000, -67, etc...
	If we wish to quit our work right now and return tomorrow, all we have to do is
	simply quit; when we wish to continue again, the reCalibrateInfo() function can
	be used to restore the original information list...

	1. We have just quit...
	2. In our current directory, we will see another directory of the form
	   Min_Heap_Tree_Files(NUMBER).BinaryT...
	3. Traverse to the Min Heap directory of the form above...
	4. Perform the following line:
	   A = reCalibrateInfo() # A is the information list...
	   Upon creating a Min-Heap for the first time, developers won't have to worry
	   about changing to the the newly created directory, as createBTO() does it for
	   them. However, if resetting an information list after an event that involved
	   quitting and leaving the directory, developers will have to traverse back to
	   the directory via additional code (the os.chdir("PATH") function works well).
	5. Should there be any deleted files from the directory, an error code will be returned...

# History:

	Version 1.0: The first version; it incorporates many of the same features as its
		     MaxHeap counterpart.

	Version 2.0: Re-Upload...