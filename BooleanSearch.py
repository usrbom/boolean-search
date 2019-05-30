import os
import email
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer 

def lemmatize_fun(lemmatizer,sentence):
	filtered_sentence = []
	for w in sentence:
			if lemmatizer.lemmatize(w)!=w:
				filtered_sentence.append(lemmatizer.lemmatize(w))
			elif lemmatizer.lemmatize(w,'v')!=w:
				filtered_sentence.append(lemmatizer.lemmatize(w,'v'))
			elif lemmatizer.lemmatize(w,'a')!=w:
				filtered_sentence.append(lemmatizer.lemmatize(w,'a'))
			elif lemmatizer.lemmatize(w,'r')!=w:
				filtered_sentence.append(lemmatizer.lemmatize(w,'r'))
			else:
				filtered_sentence.append(w)
	return filtered_sentence

def create_list(posting_list,word):
	list_new = []
	if  word not in posting_list:
		return list_new
	for element in posting_list[word]:
		if isinstance(element, basestring):
			list_new.append(element)
	return list_new

def union(posting_list,result_list,word):
	list_word = create_list(posting_list,word)
	set1 = set(list_word)
	set2 = set(result_list)
	return set1.union(set2)
	# result = set(result_list + list_word)
	# return list(result)

def merge_intersect(posting_list,result_list,word):
	list_word = create_list(posting_list,word)
	set1 = set(list_word)
	set2 = set(result_list)
	set2 = set1.intersection(set2)
	return list(set2)

def difference(posting_list,result_list,word):
	list_word = create_list(posting_list,word)
	set1 = set(list_word)
	set2 = set(result_list)
	return list(set2.difference(set1))

def print_content(filename,path):
	email_file = open(path+'/'+filename,'r')
	msg = email.message_from_file(email_file)
	# print msg['Subject']
	payload =  msg.get_payload()
	payload = unicode(payload, errors = 'ignore')
	print payload
	print "****************************************************************************************************"

if __name__ == "__main__":

	stop_words = set(stopwords.words('english'))
	stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}'])
	lemmatizer = WordNetLemmatizer() 

	freq_count = {}
	posting_list = {}


	print "Printing Documnet ids with important words after processing:"
	path = os.getcwd()+ '/DataSet/sci.space'
	printop = 1;
	for filename in os.listdir(path):
		print "Document ID: " , filename
		email_file = open(path+'/'+filename,'r')
		msg = email.message_from_file(email_file)
		# print msg['Subject']
		payload =  msg.get_payload()
		#decoding to unicode
		payload = payload.decode('utf-8','ignore')

		#####Preprocessing methods############ 
		
		#Removing Stopwords:
		temp = word_tokenize(payload)
		print temp;
	
		filtered_sentence_0 = [] 
		for w in temp: 
		    if w.lower() not in stop_words: 
		        filtered_sentence_0.append(w.lower())

		#Lemmatizing:
		filtered_sentence = lemmatize_fun(lemmatizer,filtered_sentence_0)

		#Printing the filtered important words of document		
		print filtered_sentence

		#Word frequency updation:
		for token in filtered_sentence:
			if token in freq_count: 
				freq_count[token] = freq_count[token] + 1
			else:
				freq_count[token] = 1

		#Document frequency updation:
		doc_freq = {}
		for token in filtered_sentence:
			if token in doc_freq: 
				doc_freq[token] = doc_freq[token] + 1
			else:
				doc_freq[token] = 1

		
		#Posting List Creation and Updation:
		for token in filtered_sentence:
			if token not in posting_list:
				posting_list[token] = []
			if filename not in posting_list[token]: 	
				posting_list[token].append(filename)
				posting_list[token].append(doc_freq[token])

		print "*************************"
	

	for k , v in freq_count.items():
		#Word Frequency
		print "Frequency of " , k.encode("utf-8") ," ---->", v
		#Posting List printing:
		print "The posting list of word contains list of (document id follwed by the document frequency of word) : " 
		print "Posting list -->" , posting_list[k]
		print "********"

	print len(freq_count), "is the total unique words found in dataset"	
	#Taking input here for query:
	query = raw_input("Enter Search query: ")
	print query

	#Modify query,remove stopwords and lemmatize:
	boolean_operators = {"and","or","not"}
	temp = word_tokenize(query) 
	filtered_sentence_0 = [] 
	for w in temp: 
	    if (w.lower() not in stop_words) or (w.lower() in boolean_operators):   
	        filtered_sentence_0.append(w.lower())
	print(filtered_sentence_0)
	filtered_sentence = lemmatize_fun(lemmatizer,filtered_sentence_0)
	print(filtered_sentence)

	
	#ASSUMPTIONS
	#1. Now reading sentence assuming the first and last words cannot be operators and also that two succesive words cant be operators.
	#2. Boolean operator when not used implies and operator.
	
	result_list = {}  #final posting list
	prev_word = ""    #initially no previous word
	length = len(filtered_sentence)   # length of query  
	i = 0
	while i < length:
		if i == 0:
			#inintialize result list:
			result_list = create_list(posting_list,filtered_sentence[0])
			i=i+1
			continue
		if filtered_sentence[i] in boolean_operators:
			if filtered_sentence[i] == "and":
				result_list = merge_intersect(posting_list,result_list,filtered_sentence[i+1])
				i = i+1
			elif filtered_sentence[i] == "or":
				result_list = union(posting_list,result_list,filtered_sentence[i+1]) 
				i = i+1
			else:
				result_list = difference(posting_list,result_list,filtered_sentence[i+1])
				i = i+1
		else:
			result_list = merge_intersect(posting_list,result_list,filtered_sentence[i])
		i = i+1
	
	if len(result_list) == 0:
		print "Search returned no results."
	else:
		for element in result_list:
			print_content(element,path)
	print " Number of search results = ", len(result_list)
