from flask import Flask, render_template, request,session,redirect
from flask_sqlalchemy import SQLAlchemy
import cloudinary
from flask_cors import CORS

import cloudinary.uploader
from datetime import datetime
import re

def title_to_url_format(title):
    # Remove special characters, spaces, and convert to lowercase
    cleaned_title = re.sub(r'[^a-zA-Z0-9 ]', '', title).replace(' ', '-').lower()
    url_format = f"{cleaned_title}"
    return url_format

app = Flask(__name__)
# Send a GET request to the website
# Setting data Base
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://epiz_31969556:scNLezC0sLMSr@sql307.infinityfree.com/epiz_31969556_movie'
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqlconnector://townend:krishna4704@db4free.net/townend"
CORS(app)  # Apply CORS to the entire app
cloudinary.config( 
  cloud_name = "dofvicxek", 
  api_key = "465383777877424", 
  api_secret = "a6ErazY7iy9WCT-cneQMZA7sZZQ" 
)

db = SQLAlchemy(app)
app.secret_key = "q3898c83958858g829275gj2987f987f893jf9trijwlktj398troeiu895utit875ituijti8"  # Set a secret key for session security

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    thumbnail = db.Column(db.String(200))  # Assuming it's a URL or file path
    description = db.Column(db.Text, nullable=False)
    code = db.Column(db.Text, nullable=False)
    keywords = db.Column(db.Text, nullable=False)
    type_movie = db.Column(db.Text, nullable=False)
    

    def __repr__(self):
        return f'<Resource {self.title}>'

@app.route('/')
def index():
    

    return render_template('index.html')

@app.route('/get-data/')
def getdata():
    dbms = Resource.query.all()
    raw = ''
    for item in dbms:
                # Input sentence containing keywords separated by commas
        sentence = item.keywords

        
        # Split the sentence into individual keywords
        keywords_list = sentence.split(",")
        # Print the first three keywords
        tags = ''
        try:
            for i in range(3):
                tags = f'''{tags} <span>
    <a href="/" class="h-g-primary">{keywords_list[i]}</a>
    </span>'''
        except:
            for keyword in keywords_list:
                tags = f'''{tags}  
{keyword}<!-- -->&nbsp;·&nbsp;     
                           {keyword.upper()}·
                        '''
   
        # Extract data of movie
        url = item.title
        url = title_to_url_format(url)

        raw = f"""
    <div data-test-id="web-ui-grid-item"
class="web-col web-col--4 web-col--lg-3 web-col--xl-1-5 web-col--xxl-2 web-carousel__item web-carousel__item--enable-transition">
<div data-test-id="web-ui-content-tile" class="web-content-tile">
    <div class="web-content-tile__container">
        <div class="web-content-tile__poster">
            <div class="web-poster">
                <div class="web-poster__image-container"><img class="web-poster__image-element"
                        src="{item.thumbnail}"
                        srcset="" alt="{item.title}"></div>
            </div>
        </div>
        <div class="web-content-tile__content-info">
            <div class="web-content-tile__content-digest"><a href="{url}"
                    class="web-content-tile__title">Standing
                    Ovation</a>
                <div class="web-content-tile__year-duration-rating">
                    <div class="web-content-tile__year">2010
                    </div>
                    <div class="web-content-tile__duration">1 hr
                        46 min</div>
                    <div class="web-content-tile__rating">
                        <div class="web-rating">
                            <div class="web-rating__content">PG
                            </div>
                        </div>
                    </div>
                </div>
            
            </div>
        </div>
    </div>
</div>
</div>
        
<div data-test-id="web-ui-grid-item"
    class="web-col web-col--4 web-col--lg-3 web-col--xl-1-5 web-col--xxl-2 web-carousel__item web-carousel__item--enable-transition">
    <div data-test-id="web-ui-content-tile" class="web-content-tile">
        <div class="web-content-tile__container">
            <div class="web-content-tile__poster">
                <div class="web-poster">
                    <div class="web-poster__image-container"><img class="web-poster__image-element"
                            src="{item.thumbnail}"
                            srcset="" alt=""></div>
                </div>
            </div>
            <div class="web-content-tile__content-info">
                <div class="web-content-tile__content-digest"><a href="{url}" class="web-content-tile__title">{item.title}</a>
            
                    <div class="web-content-tile__tags-row">
                        <div class="web-content-tile__tags">{tags}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{raw}"""
    return raw
@app.route('/about/')
def about():
    return render_template('about.html')
@app.route('/admin/')
def admin():
    if 'username' in session:
        username = session.get('username')
        password = session.get('password')
            # Save username and password to the session
        if username == 'shivam' and password == 'ilovecat':
            session['username'] = username
            session['password'] = password
            return redirect('/dashboard')
        if username == 'yuvraj' and password == 'yuvi123':
            session['username'] = username
            session['password'] = password
            return redirect('/dashboard')
        if username == 'krishna' and password == 'krishna4704':
            session['username'] = username
            session['password'] = password
            return redirect('/dashboard')


    return render_template('admin.html')
@app.route('/login/', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    print(username+password)
    # Save username and password to the session
    if username == 'admin' and password == 'ilovecat':
        session['username'] = username
        session['password'] = password
        return 'true'
    else:
        return 'false'
    
    
@app.route('/dashboard/')
def dashboard():
    if 'username' in session:
        username = session.get('username')
        password = session.get('password')
            # Save username and password to the session
        if username == 'admin' and password == 'ilovecat':
            session['username'] = username
            session['password'] = password
            return render_template('dashboard.html')
    return redirect('/admin')


@app.route('/upload', methods=['POST'])
def upload():
    title = request.form['title']
    description = request.form.get('description', '')  # Use get() with a default value
    download_data = request.form.getlist('list')
    tags = request.form.get('tags')
    movie_type = request.form.get('type')
    print(download_data)
    image = request.files['image']

    name1 = str(datetime.now())
    name1 = name1.replace("-", "")
    name1 = name1.replace(" ", "")
    name1 = name1.replace(":", "")
    name1 = name1.replace(".", "")
    upload_result = cloudinary.uploader.upload(image, public_id=name1)
    image_url = upload_result['secure_url']
    
    new_resource = Resource(
    title=title,
    thumbnail=image_url,
    type_movie=movie_type,
    keywords=tags,
    description=description,
    code=str(download_data)
)

    # Add the new resource to the database
    db.session.add(new_resource)
    db.session.commit()
    return 'true'
# @app.route('/m/<mo>')
@app.route('/<mo>')
def movie(mo):
    dbms = Resource.query.all()
    for item in dbms:
        title = item.title
        url = title
        url = title_to_url_format(url)
        if url == mo:
            input_string = item.code
            task  = input_string[2:-2]
            task = f'[{task}]'
            task = eval(task)
            raw = ''
            # [{'text': 'Download Gdrive', 'url': 'https://naradaic.co'}, {'text': '2ND', 'url': 'https://naradai.co/cat'}, {'text': '33', 'url': 'https://google.com'}]
            for dic in task:
        
                raw = f"""
   <p style="color: rgb(0, 183, 255);font-size: 20px; font-weight: bolder;">{dic['text']}</p>
                                        <a href="{dic['url']}" target="_blank"><button class="btn btn-primary" style="width: 7cm;">Download 1</button></a>
                                        <br>
                                        <br>{raw}
"""
            desc = item.description
            url = item.thumbnail
            return render_template('movie.html',title=title,desc=desc,url=url,raw = raw)

    return render_template('notfound.html'),404
@app.route('/pub/')
def pub():
        
    return render_template('publish.html')


if __name__ == '__main__':
    app.run(debug=True,port='8080',host="0.0.0.0")
