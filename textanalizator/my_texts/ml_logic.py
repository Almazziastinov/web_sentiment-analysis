import pickle

filename = 'C:/Users/user/Desktop/diplomka/textanalizator/my_texts/model (2) (2).h5'
loaded_model = pickle.load(open(filename, 'rb'))

new_text = "Террористический акт в Крокус Холле"

vectorizer = loaded_model.named_steps['tfidfvectorizer']
new_text_tfidf = vectorizer.transform([new_text])
def general_analiz(new_text, loaded_model):
    # Предсказание класса
    predicted = loaded_model.predict([new_text])

    # Вывод предсказанных классов
    if predicted == 'Positive':
        return 'Positive'
    else:
        return 'Negative'

def general_analiz_interface(sent_):
    return general_analiz(sent_, loaded_model)

print(general_analiz_interface(new_text))
