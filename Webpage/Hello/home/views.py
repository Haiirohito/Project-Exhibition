from django.shortcuts import render, HttpResponse
import os, json
import function.nlp as nlp
import function.scrape as scrape


# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def made_by(request):
    return render(request, 'made_by.html')

def product_question(request):
    return render(request, 'product_question.html')

def faq(request):
    return render(request, 'faq.html')

def product_result(request):
    if request.method == 'GET':
        user_input = request.GET['user_question']
        items= process_input(user_input)

        return render(request, 'product_result.html', {'items': items})


# backend function

def process_input(user_input):

    search_query = nlp.products(user_input)
    scraped_data = scrape.scrape(search_query)

    with open(f'function/data/{search_query}.json', 'w') as json_file:
        json.dump(scraped_data, json_file)


    json_file_path = os.path.join('function/data', f'{search_query}.json')
    
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as json_file:
            items = json.load(json_file)
        return items
    else:
        return "No data available for the given product."
