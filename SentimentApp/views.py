from django.shortcuts import render
from .models import SentimentModel
from .forms import SentimentForm
from code import SentimentAnalyzer
from elasticsearch import Elasticsearch


elastic = Elasticsearch(hosts=["localhost"])



# Create your views here.
def SentimentApp(request):
    form = SentimentForm(request.POST or None)
    context = {}
    if request.method == 'POST':
        if form.is_valid():
            sent = form.cleaned_data.get('Sentence')    # got the sentence
            textAns = SentimentAnalyzer(sent)
            context['result'] = textAns
            if(textAns['compound'] > 0):
                sentiment = "postive"
            elif(textAns['compound'] == 0):
                sentiment = "neutral"
            else:
                sentiment = "negative"


            # make an API call to the Elasticsearch cluster
            # and have it return a response:
            response = elastic.index(
                index="sentiment",
                doc_type="test-type",
                 body={
                       "message": sent,
                       "sentiment":sentiment,
                       "positivity": textAns['pos'],
                       "negativity": textAns['neg'],
                       "neutrality": textAns['neu'],
                       "compound": textAns['compound']
                       }
                )

            if 'acknowledged' in response:
                if response['acknowledged'] == True:
                    print ("INDEX MAPPING SUCCESS FOR INDEX:", response['index'])

            # catch API error response
            elif 'error' in response:
                print ("ERROR:", response['error']['root_cause'])
                print ("TYPE:", response['error']['type'])

            # print out the response:
            print ('\nresponse:', response)
        else:
            form = SentimentForm()
    
    context['form'] = form


    

    return render(request, 'app.html', context=context)