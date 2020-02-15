CS446 Project 1: Tokenizer
Evan Liu 02/02/2020

This Python3 program takes two files named "tokenization-input-part-A.txt"
and "tokenization-input-part-B.txt" and uses the contents of "stopwords.txt"
to process the text into tokens.

These tokens are the product of:
	1) Changing acronyms to words
	2) Removing stop words listed in "stopwords.txt"
	3) Stemming the words using Porter Stemming rules 1A and 1B

Simply run the program with the two files in the same directory and it will output two files.
The output from processing "tokenization-input-part-A.txt" will be written in file "tokenized.txt",
while the output from processing "tokenization-input-part-B.txt" will be written in file "terms.txt".

This program does not require any external dependencies that are not part of Python3's built in modules.
It does however require the "stopwords.txt" file and the two input files to be in the same directory when running.