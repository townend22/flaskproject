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
CORS(app)  # Apply CORS to the entire app
# Send a GET request to the website
# Setting data Base
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://epiz_31969556:scNLezC0sLMSr@sql307.infinityfree.com/epiz_31969556_movie'
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqlconnector://townend:krishna4704@db4free.net/townend"

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
@app.route('/sitemap.xml')
def sitemap():
    dbms = Resource.query.all()
    tm = ''
    for item in dbms:
        url = item.title
        url = title_to_url_format(url)
        current_date = datetime.now().strftime('%Y-%m-%d')

        tm = f'''<url>
<loc>https://topfilmhub.xyz/{url}</loc>
<lastmod>{current_date}</lastmod>
<changefreq>weekly</changefreq>
<priority>0.8</priority>
</url>
{tm}'''

    site = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<url>
<loc>https://topfilmhub.xyz/</loc>
<lastmod>2023-08-25</lastmod>
<changefreq>daily</changefreq>
<priority>1.0</priority>
</url>
{tm}
<!-- Add more URL entries for other pages -->
</urlset>

    '''
    
    return Response(site, content_type='text/xml')

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
   <a href="{url}"> <div data-test-id="web-ui-grid-item"
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
                    class="web-content-tile__title">{item.title}</a>
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
                <div class="web-content-tile__tags-row">
                    <div class="web-content-tile__tags">
                       {tags}
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
</div></a>
        

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


@app.route('/upload/', methods=['POST'])
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
            i = 0
            # [{'text': 'Download Gdrive', 'url': 'https://naradaic.co'}, {'text': '2ND', 'url': 'https://naradai.co/cat'}, {'text': '33', 'url': 'https://google.com'}]
            for dic in task:
                i = i + 1
                raw = f"""
{raw}
<p
    style="text-align: center; font-size: 20px;font-weight:bolder;color: rgb(95, 233, 169);background-color: #224047;padding: 15px;border-radius: 9px;width: 100%;">
    {dic['text']}</p>
<a href="{dic['url']}" id="none-react" target="_blank"><button data-test-id="web-ui-web-button" 
    class="web-button mCeMU web-button--tertiary">
    <div class="web-button__content">Download {i}
    </div>
</button></a>
"""
            description = item.description
            thumbnail = item.thumbnail

            tm = f"""
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<div>
<span style="display:none;" id = 'keywords'>{item.keywords}</span>
<span style="display:none;" id = 'deep'>{item.description}</span>
    <div class="rjiTB">
        <div class="Le3zO">
            <div class="zHQGA">
                <div class="OpEE9">
                    <div data-test-id="web-ui-grid-container" class="web-grid-container">
                        <div data-test-id="web-ui-grid-item" class="web-col web-col--3">
                            <div class="Foi1U">
                                <div class="web-poster" id="thumbnail">
                                    <div class="web-poster__image-container"><img class="web-poster__image-element"
                                            src="{thumbnail}" srcset="" alt="{title}"></div>
                                    <div class="web-poster__progress">
                                        <div class="web-poster__progress-elapsed" style="width: 0.126926%;"></div>
                                    </div>
                                </div>
                                <div class="d3O8W" id="Xx95I">
                                    <div class="ar4AE">
                                        <div class="WmxLf"><button data-test-id="web-ui-web-button"
                                                class="web-button PxzBi web-button--tertiary web-button--has-icon web-button--has-icon-no-content web-button--has-tooltip">
                                                <div data-test-id="web-ui-tooltip"
                                                    class="web-tooltip web-button__tooltip">
                                                    <div class="web-tooltip__container top dark" onclick="like()" >
                                                        Like</div><svg width="1em" height="1em" viewBox="0 0 24 24"
                                                        fill="none" xmlns="http://www.w3.org/2000/svg"
                                                        data-test-id="icons-thumb-up-stroke" role="img"
                                                        class="web-button__icon web-button__icon--no-content web-button__icon--size-large">
                                                        <title>Thumb Up Stroke Icon</title>
                                                        <path
                                                            d="M21.396 10.025C20.645 9.124 19.525 9 18.429 9H16.19C16.022 9 15.904 8.834 15.953 8.673C16.291 7.55 16.312 7.07 16.312 5.383V4.707C16.312 3.214 15.125 2 13.666 2H13.315C12.136 2 11.089 2.811 10.77 3.971L10.549 4.771C10.147 6.229 9.477 7.566 8.558 8.746C8.471 8.858 8.335 8.923 8.187 8.96C7.639 8.373 6.865 8 6 8H5C3.343 8 2 9.343 2 11V18C2 19.657 3.343 21 5 21H6C6.848 21 7.611 20.643 8.157 20.076C8.785 20.644 9.616 21 10.544 21H16.665C17.714 21 18.813 20.891 19.747 20.096C20.718 19.271 20.981 18.167 21.152 17.196L21.866 13.156C22.045 12.135 22.172 10.967 21.396 10.025ZM7 18C7 18.551 6.551 19 6 19H5C4.449 19 4 18.551 4 18V11C4 10.449 4.449 10 5 10H6C6.551 10 7 10.449 7 11V18ZM19.896 12.81L19.183 16.849C19.014 17.806 18.823 18.257 18.451 18.573C18.08 18.888 17.613 19 16.665 19H10.5C9.673 19 9 18.327 9 17.5V11C9 10.933 8.984 10.869 8.98 10.803C9.431 10.631 9.838 10.356 10.135 9.976C11.218 8.587 12.005 7.015 12.477 5.303L12.698 4.503C12.779 4.207 13.033 4 13.315 4H13.666C14.021 4 14.312 4.317 14.312 4.707V5.383C14.312 7.299 14.312 7.299 13.715 9.103C13.567 9.548 13.639 10.039 13.91 10.415C14.174 10.781 14.602 11 15.054 11H18.429C19.253 11 19.682 11.092 19.857 11.302C20.035 11.518 20.046 11.955 19.896 12.81Z"
                                                            fill="currentColor"></path>
                                                    </svg><p id="like"></p>
                                                </div>
                                            </button><button data-test-id="web-ui-web-button"
                                                class="web-button PxzBi web-button--tertiary web-button--has-icon web-button--has-icon-no-content web-button--has-tooltip">
                                                <div data-test-id="web-ui-tooltip"
                                                    class="web-tooltip web-button__tooltip">
                                                    <div class="web-tooltip__container top dark" onclick="dislike()" id="dislike">
                                                        Dislike</div><svg width="1em" height="1em" viewBox="0 0 24 24"
                                                        fill="none" xmlns="http://www.w3.org/2000/svg"
                                                        data-test-id="icons-thumb-down-stroke" role="img"
                                                        class="web-button__icon web-button__icon--no-content web-button__icon--size-large">
                                                        <title>Thumb Down Stroke Icon</title>
                                                        <path
                                                            d="M21.8646 10.844L21.1507 6.804C20.9797 5.833 20.7157 4.729 19.7458 3.904C18.8118 3.109 17.7129 3 16.664 3H10.5434C9.61547 3 8.78453 3.356 8.15658 3.924C7.61061 3.357 6.84767 3 5.99973 3H4.99979C3.34291 3 2 4.343 2 6V13C2 14.657 3.34291 16 4.99979 16H5.99973C6.86467 16 7.63861 15.627 8.18657 15.04C8.33456 15.078 8.47055 15.142 8.55755 15.254C9.47648 16.434 10.1464 17.771 10.5484 19.229L10.7694 20.029C11.0884 21.189 12.1353 22 13.3142 22H13.6652C15.1241 22 16.311 20.786 16.311 19.293V18.617C16.311 16.93 16.291 16.449 15.952 15.327C15.903 15.166 16.021 15 16.189 15H18.4269C19.5238 15 20.6427 14.876 21.3947 13.975C22.1706 13.033 22.0436 11.865 21.8646 10.844ZM6.99966 13C6.99966 13.551 6.55069 14 5.99973 14H4.99979C4.44883 14 3.99986 13.551 3.99986 13V6C3.99986 5.449 4.44883 5 4.99979 5H5.99973C6.55069 5 6.99966 5.449 6.99966 6V13ZM19.8548 12.698C19.6808 12.908 19.2518 13 18.4279 13H15.0531C14.6011 13 14.1732 13.219 13.9092 13.586C13.6382 13.962 13.5652 14.452 13.7142 14.898C14.3112 16.702 14.3112 16.702 14.3112 18.618V19.294C14.3112 19.684 14.0212 20.001 13.6652 20.001H13.3142C13.0322 20.001 12.7783 19.794 12.6973 19.498L12.4763 18.698C12.0043 16.986 11.2164 15.413 10.1344 14.025C9.83846 13.645 9.43149 13.371 8.97952 13.198C8.98352 13.131 8.99952 13.067 8.99952 13V6.5C8.99952 5.673 9.67247 5 10.4994 5H16.664C17.6119 5 18.0789 5.112 18.4499 5.428C18.8218 5.743 19.0128 6.195 19.1818 7.152L19.8948 11.191C20.0448 12.045 20.0338 12.482 19.8548 12.698Z"
                                                            fill="currentColor"></path>
                                                    </svg>
                                                </div>
                                            </button></div>
                                    </div>
                                    {raw}
                                    <div class="ar4AE">
                                        <!-- <div class="XByGK"><button data-test-id="web-ui-web-button"
                                                class="web-button H5RWw web-button--tertiary">
                                                <a href="https://api.whatsapp.com/send?text=Google%20vs.%20Microsoft:%20A%20Battle%20for%20Tech%20Supremacy%20|%20https://www.dinoblogs.online/2023/06/google-vs-microsoft-battle-for-tech.html" target="_blank"><div class="web-button__content" style="text-align: center;" >Share</div>
                                                </div>
                                            </button></div> -->
                                        <!-- <div class="un53Z"><button data-test-id="web-ui-web-button"
                                                class="web-button XykWo web-button--tertiary">
                                                <div class="web-button__content" style="text-align: center;"><svg
                                                        width="1em" height="1em" viewBox="0 0 24 24" fill="none"
                                                        xmlns="http://www.w3.org/2000/svg" class="mTKCf">
                                                        <path fill-rule="evenodd" clip-rule="evenodd"
                                                            d="M9 12C9 11.4477 8.55228 11 8 11C7.44772 11 7 11.4477 7 12C7 12.5523 7.44772 13 8 13C8.55228 13 9 12.5523 9 12ZM12 11C12.5523 11 13 11.4477 13 12C13 12.5523 12.5523 13 12 13C11.4477 13 11 12.5523 11 12C11 11.4477 11.4477 11 12 11ZM16 11C16.5523 11 17 11.4477 17 12C17 12.5523 16.5523 13 16 13C15.4477 13 15 12.5523 15 12C15 11.4477 15.4477 11 16 11Z"
                                                            fill="currentColor"></path>
                                                    </svg></div>
                                            </button></div> -->
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div data-test-id="web-ui-grid-item" id="mov1" class="web-col web-col--sm-12 web-col--lg-9">
                            <h1 class="c1jX9" id="mv-title">{title}</h1>
                            <div class="web-attributes">
                                <div class="web-attributes__meta"><span>2017 · 1 hr 31 min</span>
                                    <div class="web-attributes__rating-descriptor">
                                        <div class="web-attributes__rating">
                                            <div class="web-attributes__badge">PG</div>
                                        </div>
                                    </div>
                                </div>
                                <div>{tags}</div>
                            </div>
                            <div class="Xx95I">
                                <pre style="white-space: pre-wrap;word-wrap: break-word;">{description}</pre>
                            </div>
                            <!-- <div class="LXnxs">
                                <div class="Em3_m"><span class="Cg14t">Starring</span><span><a class="ATag"
                                            href="/person/71655e/pappy-faulkner"><span class="KJR4e">Pappy
                                                Faulkner</span></a><a class="ATag"
                                            href="/person/f88957/christopher-j-parson"><span class="KJR4e">Christopher
                                                J. Parson</span></a><a class="ATag"
                                            href="/person/5cb530/joey-camen"><span class="KJR4e">Joey
                                                Camen</span></a></span></div>
                                <div class="Em3_m"><span class="Cg14t">Directed by</span><span><a class="ATag"
                                            href="/person/398c30/jeremy-degruson"><span class="KJR4e">Jeremy
                                                Degruson</span></a><a class="ATag"
                                            href="/person/7e41c8/ben-stassen"><span class="KJR4e">Ben
                                                Stassen</span></a></span></div>
                            </div> -->
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>


</div>
<div></div>

<div></div>
</div>
</div>
</div>




"""
            return tm

    return 'Not Found'
@app.route('/get/<mo>')
def topuo(mo):
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
            i = 0
            # [{'text': 'Download Gdrive', 'url': 'https://naradaic.co'}, {'text': '2ND', 'url': 'https://naradai.co/cat'}, {'text': '33', 'url': 'https://google.com'}]
            for dic in task:
                i = i + 1
                raw = f"""
   <p style="color: rgb(0, 183, 255);font-size: 20px; font-weight: bolder;">{dic['text']}</p>
                                        <a href="{dic['url']}" target="_blank"><button class="btn btn-primary" style="width: 7cm;">Download {i}</button></a>
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
