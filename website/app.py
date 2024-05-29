
class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    performer = db.Column(db.String(100), nullable=False)
    chart_debut = db.Column(db.String(500), nullable=False)
    peak_position = db.Column(db.Integer, nullable=False)
    time_on_chart = db.Column(db.Integer, nullable=False)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    feedback = db.Column(db.Text, nullable=False)

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/search")
def search():
    q = request.args.get("q")
    results = []
    
    if q:
        # Search in Song model
        song_results = Song.query.filter(Song.title.ilike(f'%{q}%') | Song.performer.ilike(f'%{q}%')).all()
        for song in song_results:
            results.append({
                "type": "Song",
                "title": song.title,
                "performer": song.performer,
                "chart_debut": song.chart_debut,
                "peak_position": song.peak_position,
                "time_on_chart": song.time_on_chart
            })

        # Search in Blog model
        blog_results = Blog.query.filter(Blog.title.ilike(f'%{q}%') | Blog.content.ilike(f'%{q}%')).all()
        for blog in blog_results:
            results.append({
                "type": "Blog",
                "title": blog.title,
                "content": blog.content[:200] + "..."  # Only show first 200 characters
            })

        # Search in Feedback model
        feedback_results = Feedback.query.filter(Feedback.user_name.ilike(f'%{q}%') | Feedback.feedback.ilike(f'%{q}%')).all()
        for feedback in feedback_results:
            results.append({
                "type": "Feedback",
                "user_name": feedback.user_name,
                "feedback": feedback.feedback[:200] + "..."  # Only show first 200 characters
            })

    return jsonify(results)

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    db.init_app(app)
    app.register_blueprint(main)
    
    with app.app_context():
        db.create_all()  # Ensure the database tables are created

    return app