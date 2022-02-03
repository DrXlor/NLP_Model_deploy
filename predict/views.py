from django.shortcuts import render
from django.http import JsonResponse
from pandas import read_pickle
from .models import PredResults
from sklearn.feature_extraction.text import TfidfVectorizer
import os


def predict(request):
    return render(request, 'predict.html')


def predict_chances(request):
    if request.POST.get('action') == 'post':
        # Receive data from client
        review = str(request.POST.get('review'))

        # Unpickle models & vectorizer's vocab
        tone_model = read_pickle("predict/tone_model.pkl")
        score_model = read_pickle("predict/score_model.pkl")
        vocab = read_pickle("predict/vect_vocab.pkl")
        vectorizer = TfidfVectorizer(vocabulary=vocab)

        # Make prediction
        vectorized_review = vectorizer.fit_transform([review])
        tone_result = tone_model.predict(vectorized_review)
        score_result = score_model.predict(vectorized_review)

        tone_classification = str(tone_result[0])
        score_classification = str(score_result[0])

        PredResults.objects.create(review=review,
                                   tone_classification=tone_classification,
                                   score_classification=score_classification)

        print(os.environ.get('NAME'))

        return JsonResponse({'tone_result': tone_classification,
                             "score_result": score_classification,
                             "review": review},
                            safe=False)


def view_results(request):
    # Submit prediction and show all
    data = {"dataset": PredResults.objects.all()}
    return render(request, "results.html", data)
