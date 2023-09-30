import spacy
from goose3 import Goose
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from wordcloud import WordCloud
import matplotlib.pyplot as plt

class ChatbotLogic:
    def __init__(self):
        #inicialização
        #nltk.download('punkt')

        self.nlp = spacy.load("pt_core_news_sm")
        self.g = Goose()

        # Lista de URLs dos artigos
        urls = [
            "https://www.dicio.com.br/pizza/",
            "https://gauchazh.clicrbs.com.br/destemperados/tendencias/noticia/2021/07/pizza-e-realmente-de-origem-italiana-descubra-a-verdadeira-historia-sobre-a-origem-do-classico-ckqvavi15006j013brqvi7pcf.html",
            "https://redeglobo.globo.com/redebahia/noticia/historia-da-pizza-descubra-como-surgiu-o-prato-que-e-tao-popular-entre-os-brasileiros.ghtml",
            "https://pt.wikipedia.org/wiki/Pizza",
            "https://gastronomiaitaliana.com.br/a-historia-da-pizza/",
        ]

        article_texts = []

        #Extrair os artigos da lista
        for url in urls:
            article = self.g.extract(url)
            article_texts.append(article.cleaned_text)

        #Combinar todos os artigos antes de tokenizar
        self.combined_articles = '\n'.join(article_texts)

        self.original_sentences = [sentence for sentence in nltk.sent_tokenize(self.combined_articles)]

    #faz o preprocessing do artigo que foi recebido
    def preprocessing(self, sentence):
        sentence = sentence.lower()
        
        #usando lematização
        tokens = [token.lemma_ for token in self.nlp(sentence) if not (token.is_stop or token.like_num or token.is_punct or token.is_space or len(token) == 1)]

        return ' '.join(tokens)
    
    #cria a nuvem de palavras com o texto já limpo pelo preprocessing
    def createWordCloud(self):
        cloud = WordCloud()
        wordcloud = cloud.generate(self.preprocessing(self.combined_articles))
        plt.figure(figsize=(8, 8))
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.show()

    #função onde o bot responde a pergunta do usuário.
    #se a similaridade for < 0.15, o bot não é capaz de responder.
    def answer(self, user_text, threshold=0.15):
        cleaned_sentences = [self.preprocessing(sentence) for sentence in self.original_sentences]
        user_text = self.preprocessing(user_text)
        cleaned_sentences.append(user_text)

        tfidf = TfidfVectorizer()
        x_sentences = tfidf.fit_transform(cleaned_sentences)

        similarity = cosine_similarity(x_sentences[-1], x_sentences)
        sentence_index = similarity.argsort()[0][-2]

        chatbot_answer = ''

        user_messages_possibilities = ['oi', 'ola', 'olá']

        if user_text.lower() in user_messages_possibilities:
            chatbot_answer += "Oi! Qual sua pergunta?"

        elif user_text == "":
             chatbot_answer += "Digite uma pergunta para que eu possa respondê-la."
             
        elif similarity[0][sentence_index] < threshold:
            chatbot_answer += "Desculpe, ainda não consigo responder isso. Tente outra pergunta!"
        else:
            chatbot_answer += self.original_sentences[sentence_index]

        return chatbot_answer