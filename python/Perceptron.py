from __future__ import division  
import sys
import getopt
import os
import math
import operator
from random import shuffle

class Perceptron:
  class TrainSplit:
    """Represents a set of training/testing data. self.train is a list of Examples, as is self.test. 
    """
    def __init__(self):
      self.train = []
      self.test = []

  class Example:
    """Represents a document with a label. klass is 'pos' or 'neg' by convention.
       words is a list of strings.
    """
    def __init__(self):
      self.klass = ''
      self.words = []


  def __init__(self):
    """Perceptron initialization"""
    self.numFolds = 10
    self.D = 0
    self.c = 1
    self.weights = {}
    self.avg_weights = {}
    self.word_occurence = {}
    self.bias = 0
    self.avg_bias = 0
  #############################################################################
  # TODO TODO TODO TODO TODO 
  # Implement the Perceptron classifier 

  weights = {}
  avg_weights = {}
  word_occurence = {}
  bias = 0
  avg_bias = 0
  c = 1
  D = 0 #Total document counts
  def classify(self, words):
    """ TODO
      'words' is a list of words to classify. Return 'pos' or 'neg' classification.
    """

    # Write code here
    vector = self.makeSentenceVectors(words)

    total_value = self.calFunctionOfX(vector)
    
    
    if(total_value > 0): return 'pos'
    else: return 'neg'

  def isPositive(self, y):
      if(isinstance(y, basestring)):
          if(y == 'pos'):
              return 1
          else:
              return -1
      else:
          if(y >= 0):
              return 1
          else:
              return -1

  def makeSentenceVectors(self, words):
    dic = {} # [Words:num of occurence]
    idf = {}
    tf_idf = {}
    for w in words:
        if(dic.has_key(w)):
            dic[w] += 1
        else:
            dic[w] = 1

    for key in dic:
        idf[key] = 1
        if(self.word_occurence.has_key(key)):
            idf[key] += self.word_occurence[key]
        idf[key]  = math.log10(self.D/idf[key])
        tf_idf[key] = (dic[key]/len(words))*idf[key]

    return tf_idf
  
  def calFunctionOfX(self, vector):
    total_value = 0
    for key in vector:
        if(self.weights.has_key(key)==False):
            self.weights[key] = 0
        if(self.avg_weights.has_key(key)==False):
            self.avg_weights[key] = 0
        total_value += vector[key]*self.weights[key]
    total_value += self.bias
    return total_value

  def updateWeights(self, y, y_hat, vector):
    if(y != y_hat):
        for key in vector:
            #self.weights[key] += (y-y_hat)*vector[key]
            self.weights[key] += y*vector[key]
            #self.avg_weights[key] += self.c*(y-y_hat)*vector[key]
            self.avg_weights[key] += self.c*y*vector[key]

        self.bias += y
        self.avg_bias += self.c*y
    self.c += 1

#if a word occures in the sentence, self.word_occurence[word]+1
  def calWordsOccurence(self, train):
      
      for example in train:
        words = example.words
        tmp = {}
        for w in words:
          tmp[w] = 1
        for key in tmp:
          if(self.word_occurence.has_key(key)):
              self.word_occurence[key] += 1
          else:
              self.word_occurence[key] = 1

  def addExample(self, klass, words):
    """
     * TODO
     * Train your model on an example document with label klass ('pos' or 'neg') and
     * words, a list of strings.
     * You should store whatever data structures you use for your classifier 
     * in the Perceptron class.
     * Returns nothing
    """
    # Write code here
    y = self.isPositive(klass)
    vector = self.makeSentenceVectors(words)
    total_value = self.calFunctionOfX(vector)
    self.updateWeights(y, self.isPositive(total_value), vector)

    pass
  
  def train(self, split, iterations):
      """
      * TODO 
      * iterates through data examples
      * TODO 
      * use weight averages instead of final iteration weights
      """
      #Precalculate the words occurences in the whole dataset
      self.calWordsOccurence(split.train)

      self.D = len(split.train)
      
      shuffle(split.train)
      for _ in range(iterations):
        for example in split.train:
            words = example.words
            self.addExample(example.klass, words)
      

  # END TODO (Modify code beyond here with caution)
  #############################################################################
  
  
  def readFile(self, fileName):
    """
     * Code for reading a file.  you probably don't want to modify anything here, 
     * unless you don't like the way we segment files.
    """
    contents = []
    f = open(fileName)
    for line in f:
      contents.append(line)
    f.close()
    result = self.segmentWords('\n'.join(contents)) 
    return result

  
  def segmentWords(self, s):
    """
     * Splits lines on whitespace for file reading
    """
    return s.split()

  
  def trainSplit(self, trainDir):
    """Takes in a trainDir, returns one TrainSplit with train set."""
    split = self.TrainSplit()
    posTrainFileNames = os.listdir('%s/pos/' % trainDir)
    negTrainFileNames = os.listdir('%s/neg/' % trainDir)
    for fileName in posTrainFileNames:
      example = self.Example()
      example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
      example.klass = 'pos'
      split.train.append(example)
    for fileName in negTrainFileNames:
      example = self.Example()
      example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
      example.klass = 'neg'
      split.train.append(example)
    return split


  def crossValidationSplits(self, trainDir):
    """Returns a lsit of TrainSplits corresponding to the cross validation splits."""
    splits = [] 
    posTrainFileNames = os.listdir('%s/pos/' % trainDir)
    negTrainFileNames = os.listdir('%s/neg/' % trainDir)
    #for fileName in trainFileNames:
    for fold in range(0, self.numFolds):
      split = self.TrainSplit()
      for fileName in posTrainFileNames:
        example = self.Example()
        example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
        example.klass = 'pos'
        if fileName[2] == str(fold):
          split.test.append(example)
        else:
          split.train.append(example)
      for fileName in negTrainFileNames:
        example = self.Example()
        example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
        example.klass = 'neg'
        if fileName[2] == str(fold):
          split.test.append(example)
        else:
          split.train.append(example)
      splits.append(split)
    return splits
  

def test10Fold(args):
  pt = Perceptron()
  
  iterations = int(args[1])
  splits = pt.crossValidationSplits(args[0])
  avgAccuracy = 0.0
  fold = 0
  for split in splits:
    classifier = Perceptron()
    accuracy = 0.0
    classifier.train(split,iterations)
  
    for example in split.test:
      words = example.words
      guess = classifier.classify(words)
      if example.klass == guess:
        accuracy += 1.0

    accuracy = accuracy / len(split.test)
    avgAccuracy += accuracy
    print '[INFO]\tFold %d Accuracy: %f' % (fold, accuracy) 
    fold += 1
  avgAccuracy = avgAccuracy / fold
  print '[INFO]\tAccuracy: %f' % avgAccuracy
    
    
def classifyDir(trainDir, testDir,iter):
  classifier = Perceptron()
  trainSplit = classifier.trainSplit(trainDir)
  iterations = int(iter)
  classifier.train(trainSplit,iterations)
  testSplit = classifier.trainSplit(testDir)
  #testFile = classifier.readFile(testFilePath)
  accuracy = 0.0
  for example in testSplit.train:
    words = example.words
    guess = classifier.classify(words)
    if example.klass == guess:
      accuracy += 1.0
  accuracy = accuracy / len(testSplit.train)
  print '[INFO]\tAccuracy: %f' % accuracy
    
def main():
  (options, args) = getopt.getopt(sys.argv[1:], '')
  
  if len(args) == 3:
    classifyDir(args[0], args[1], args[2])
  elif len(args) == 2:
    test10Fold(args)

if __name__ == "__main__":
    main()
