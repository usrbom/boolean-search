# boolean-search

Boolean Search Model is a classic Information Retrieval(IR) Model based on Boolean Logic and classical set theory in that both the documents to be searched and the user's query are conceived as sets of terms. Retrieval is based on whether or not the documents contain the query terms.(Refer https://en.wikipedia.org/wiki/Boolean_model_of_information_retrieval)

## Process:

### 1. **Information Extraction**
	- Our source of information will be the 20 Newsgroup Dataset.
	- For demonstration we would be using the sci.space Dataset in it only for now.
	- Our aim will be to create posting lists which is basically collecting all the unique terms from this dataset and making a linked lists of all terms containg their document ids in an ordered manner.

### 2. **Data Preprocessing**
	- We will apply stopword removal, and lemmatization (stemming can also be used).
	- We will be using the nltk python library for this.
	- We do this for each document creating the posting lists of terms in it simultaneously.

### 3. **Information Retrieval**
	- A query can contain words and 3 operators(AND, OR & NOT).
	- We allow the user to enter a search query with the assumption that:
		- First and last words cannot be operators. 
		- Two succesive words cant be operators.
		- Boolean operator when not used between words implies AND operator.
	- We merge the posting lists of the terms entered in query and display the intersecting resulting pages accordingly. 

## **To Run**:

Keep the file containg dataset along with BooleanSearch.py
Install dependancies from terminal: 
```
$sudo pip install -U nltk
```
To run the program:
```
$python2 BooleanSearch.py
```
Input query when prompted.<br/>
example: astronomer and moon not stars.

