from flask import render_template, flash, redirect, url_for
from app import app
from forms import EditForm
import requests


@app.route('/', methods = ['GET', 'POST'])
def index():
    form = EditForm()
    if form.validate_on_submit():
        #request conceptnet5
        term_field = form.terms.data
        terms = ','.join([x.strip() for x in term_field.split(',')]).replace(' ','_')
        concept_url = 'http://conceptnet5.media.mit.edu/data/5.2/assoc/list/en/'+terms+'?limit=10&filter=/c/en'
        response = requests.get(concept_url)
        data = response.json()
        #extract answer terms
        similar = data[u'similar']
        #print similar
        if len(similar) > 0:
            answers = [x[0].encode().split('/')[3] for x in similar]
            keywords = [x for x in answers if x not in terms] 
            google_q = keywords[0].replace('_','+')
            #request google images
            google_url = 'https://www.googleapis.com/customsearch/v1?key=AIzaSyCqVvCxoKA6GKGcr_2kYqFg2O3E-kof2-c&cx=003867484209474582163:3ikgk4xehfo' +\
            '&searchType=image&fileType=jpg&imgSize=small&alt=json&q='+google_q
            response = requests.get(google_url)
            data = response.json()
            link = data[u'items'][0][u'link']
            message = "ConceptNet5 association request: ("+ terms+"), results: "+', '.join(keywords)
            return render_template('base.html',
                form = form,
                link = link,
                image_title = keywords[0],
                message = message,
                title = 'ConceptApp')
        else:
            return render_template('base.html',
                form = form,
                message = "No results from conceptnet5",
                title = 'ConceptApp')
    return render_template('base.html',
        form = form,
        title = 'ConceptApp')