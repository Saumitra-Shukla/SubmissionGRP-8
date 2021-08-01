from django.shortcuts import render
from .models import Preference,Newspaper_name,News
# Create your views here.
from django.views.generic import View,TemplateView,ListView,DetailView
import csv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()


class NewsListView(ListView):
	model = News
	context_object_name = 'news'
	#template_name = 'newspaper/newspaper_detail.html
	def get_queryset(self):
		now = timezone.now()
		upcoming = News.objects.filter(date__gte=now).order_by('date')
		passed = News.objects.filter(date__lte=now).order_by('-date')
		return list(upcoming) + list(passed)

def news_detail_view(request, pk):

	newspaper= Newspaper_name.objects.filter(pk=pk)
	print(newspaper)
	# news = newspaper.related_news.all
	news=list(News.objects.filter(newspaper_name_id=int(pk)))
	print(news)
	return render(request, 'newspapers/newspaper_detail.html',{'news': news,'newspaper':newspaper,'names':Newspaper_name.objects.all().order_by('-id')})

def vader_sentiment(request):
	news_new=[]
	index=[]
	senti_comp=[]
	final_index=[]
	read = News.objects.all()
	i=1
	for x in read:
		news_new.append(x)
		sentence =x.article
		my_dict=analyser.polarity_scores(sentence)
		senti_comp.append(my_dict['compound'])
		# print(senti_comp)
		index.append(i)
		i+=1
	senti_comp, index = zip(*sorted(zip(senti_comp,index)))
	print(senti_comp)
	print(index[0])
	j= -0.5000
	k=0
	final_index=[]

	for i in senti_comp:
		if i<=j:
			final_index.append(index[k])
		k+=1
	print(final_index,index)
	j= 0.5000
	k=0
	# final_index=[]

	for i in senti_comp:
		if i>j:
			final_index.append(index[k])
		k+=1
	# print(final_index)
	j= -0.5000
	k=0
	# final_index2=[]

	for i in senti_comp:
		if i <0 and i > j:
			final_index.append(index[k])
		k+=1
	# print(final_index2)
	j= 0.5000
	k=0
	# final_index3=[]

	for i in senti_comp:
		if i >0 and i< j:
			final_index.append(index[k])
		k+=1
	# print(final_index3)
	j=0.0
	k=0
	# final_index4=[]

	for i in senti_comp:
		if i == j:
			final_index.append(index[k])
		k+=1
	# print(final_index4)
	#print(final_index)
	news_new_final=[]
	for i in final_index:
		print(type(news_new[i-1]))
		news_new_final.append(news_new[i-1])
	return render(request, 'newspapers/preriority.html',{'news': news_new_final})


def latest_news(request):
	news=News.objects.all().order_by("-id")[:6]
	return render(request,'newspapers/latest.html',context={'news':news})


def create_summary(text):
	# importing libraries
	import nltk
	from nltk.corpus import stopwords
	from nltk.tokenize import word_tokenize, sent_tokenize

	# Tokenizing the text
	stopWords = set(stopwords.words("english"))
	words = word_tokenize(text)

	# Creating a frequency table to keep the
	# score of each word

	freqTable = dict()
	for word in words:
		word = word.lower()
		if word in stopWords:
			continue
		if word in freqTable:
			freqTable[word] += 1
		else:
			freqTable[word] = 1

	# Creating a dictionary to keep the score
	# of each sentence
	sentences = sent_tokenize(text)
	sentenceValue = dict()

	for sentence in sentences:
		for word, freq in freqTable.items():
			if word in sentence.lower():
				if sentence in sentenceValue:
					sentenceValue[sentence] += freq
				else:
					sentenceValue[sentence] = freq

	sumValues = 0
	for sentence in sentenceValue:
		sumValues += sentenceValue[sentence]

	# Average value of a sentence from the original text

	average = int(sumValues / len(sentenceValue))

	# Storing sentences into our summary.
	summary = ''
	for sentence in sentences:
		if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
			summary += " " + sentence
	return summary

def get_summary(request,pk):
	news_obj = News.objects.get(id=pk)
	summary_text = create_summary(news_obj.article)
	news_obj.summary=summary_text
	return render(request,'newspapers/news.html',{"news_detail":news_obj})


class NewsDetailView(DetailView):
	sample_dict = {}
	for i in range(100):
		for j in range(100):
			sample_dict[str(j) + "_" + str(i)] = j

	model = News
	context_object_name = 'news_detail'
	template_name = 'newspapers/news.html'

	def post(self, request,pk):
		return get_summary(request,pk)
