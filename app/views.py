# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView
from home.forms import HomeForm
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from heapq import nlargest
from nltk.corpus import stopwords
from nltk import PunktSentenceTokenizer
from nltk.tokenize import sent_tokenize, word_tokenize
import string
from collections import defaultdict
import spacy


class HomeView(TemplateView):
    template_name = 'html/index.html'
    template1_name = 'html/result.html'

    def get(self, request):
        form = HomeForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = HomeForm(request.POST)
        if form.is_valid():
            firstPassage = form.cleaned_data['firstPassage']
            secondPassage = form.cleaned_data['secondPassage']
            x = 0
            i = 0
            j = 0
            ratio = 0
            firstPassage1 = firstPassage.split( )
            secondPassage1 = secondPassage.split( )
            for index in firstPassage1:
                #if wordcount == " ":
                i+=1
            for index in secondPassage1:
                #if wordcount == " ":
                j+=1

            if i > j:
                ratio = i-j
                flag = firstPassage
                sflag = secondPassage
            elif j>i:
                ratio = j-i
                flag = secondPassage
                sflag = firstPassage

            if ratio > 50  :
                min_cut = 0.1
                max_cut = 0.9
                stopwrds = set(stopwords.words('english')+list(string.punctuation))
                sentences = sent_tokenize(flag)
                smallpass = sent_tokenize(sflag)
                n = len(smallpass)
                word_sent = [word_tokenize(s.lower()) for s in sentences]
                freq = defaultdict(int)
                for sentence in word_sent:
                    for word in sentence:
                        if word not in stopwrds:
                            freq[word] += 1
                m = float(max(freq.values()))
                for word in freq.keys():
                    freq[word] = freq[word]/m
                    if freq[word] >= max_cut or freq[word] <= min_cut:
                        del freq[word]
                ranking = defaultdict(int)
                for k,sentence in enumerate(word_sent):
                    for word in sentence:
                        if word in freq:
                            ranking[k] += freq[word]

                sentences_index = nlargest(n, ranking , key = ranking.get)
                sentences_index2 = (str)(sentences_index)
                passage_sum = ""
                for l in sentences_index:
                    passage_sum += "%s "%(sentences[l])
                passage_sum1 = passage_sum.split( )
                for a in passage_sum1:
                    x += 1
                if flag == firstPassage:
                    firstPassage = passage_sum
                else:
                    secondPassage = passage_sum
            vect = TfidfVectorizer(min_df = 1)
            tfidf = vect.fit_transform([firstPassage,secondPassage])
            result3 = ((tfidf * tfidf.T).A)
            result4 = 100 - (int)(result3[1,0]*100)
            return render(request, self.template1_name, {'result3' : (int)(result3[1,0]*100), 'result4' : result4, 'fwordcount' : i , 'swordcount' : j, 'summarized' : x})
