from flask import render_template, flash, redirect, url_for
from app import app
from forms import EditForm
import requests


@app.route('/', methods = ['GET', 'POST'])
def index():
    form = EditForm(csrf_enabled = False)
    if form.validate_on_submit():
        #request conceptnet5
        term_field = form.terms.data
        terms = ','.join([x.strip() for x in term_field.split(',')]).replace(' ','_')
        concept_req = ', '.join(terms.split(','))
        concept_url = 'http://conceptnet5.media.mit.edu/data/5.2/assoc/list/en/'+terms+'?limit=10&filter=/c/en'
        response = requests.get(concept_url)
        data = response.json()
        #extract answer terms
        similar = data[u'similar']
        #print similar
        if len(similar) > 0:
            answers = [x[0].encode().split('/')[3] for x in similar]
            keywords = [x for x in answers if x not in terms]
            concept_ans = ', '.join(keywords)            
            google_q = keywords[0].replace('_','+')
            #request google images
            CONCEPTAPP_API_KEY = app.config['CONCEPTAPP_API_KEY']
            CONCEPTAPP_CSE_ID = app.config['CONCEPTAPP_CSE_ID']
            google_url = 'https://www.googleapis.com/customsearch/v1?key='+ CONCEPTAPP_API_KEY +'&cx=' +CONCEPTAPP_CSE_ID +\
            '&searchType=image&fileType=jpg&imgSize=medium&alt=json&q='+google_q
            response = requests.get(google_url)
            data = response.json()
            if u'error' in data:
                return render_template('index.html',
                    form = form,
                    concept_req=concept_req,
                    concept_ans = concept_ans,
                    google_error = data[u'error'][u'errors'][0][u'message'],
                    title = 'ConceptApp')               
            link = data[u'items'][0][u'link']
            return render_template('index.html',
                form = form,
                link = link,
                image_title = keywords[0],
                concept_req= concept_req,
                concept_ans = concept_ans,
                title = 'ConceptApp')
        else:
            return render_template('index.html',
                form = form,
                concept_req =concept_req,
                concept_error = "No results from conceptnet5",
                title = 'ConceptApp')
    return render_template('index.html',
        form = form,
        title = 'ConceptApp')