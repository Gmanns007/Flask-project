from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import current_user, login_required
from .models import Post, User, Journal #UploadMedia
from . import db
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename 
import uuid as uuid
import os 

views = Blueprint("views", __name__)


@views.route("/")
def firstPage():
    return render_template("index.html")


@views.route("/home")
@login_required
def home():
    posts = Post.query.all()
    return render_template("posts.html", user=current_user, posts=posts)


@views.route("/introduction")
@login_required
def introduction_posts():
    posts = Post.query.all()
    return render_template("introduction_posts.html", user=current_user, posts=posts)


@views.route("/introduction-modal")
@login_required
def introduction_modal():
    posts = Post.query.all()
    return render_template("introduction_modal.html", user=current_user, posts=posts)


@views.route("/outsideView")
def logout():
    return render_template("logout.html", user=current_user)


@views.route("/CreatePost", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')
        audio = request.files["audio"]
        video = request.files["video"]
        image = request.files["image"]
        if audio == "<FileStorage: '' ('application/octet-stream')>":
            audio = None

        if video == "<FileStorage: '' ('application/octet-stream')>":
            video = None

        if image == "<FileStorage: '' ('application/octet-stream')>":
            image = None

        #image storage
        image_filename = secure_filename(image.filename)
        print(image_filename)
        if image_filename == '':
            image_name = None
        else:
            image_name = str(uuid.uuid1()) + "_" + image_filename
            print(image_name)

        image_saver = request.files['image']

        #video storage
        video_filename = secure_filename(video.filename)
        print(video_filename)
        if video_filename == '':
            video_name = None
        else:
            video_name = str(uuid.uuid1()) + "_" + video_filename
            print(video_name)

        video_saver = request.files['video']

        #audio storage
        audio_filename = secure_filename(audio.filename)
        print(audio_filename)
        if audio_filename == '':
            audio_name = None
        else:
            audio_name = str(uuid.uuid1()) + "_" + audio_filename
            print(audio_name)

        audio_saver = request.files['audio']

        if not text:
            flash('Post cannot be empty', category='error')
        else:
            post = Post(text=text, author=current_user.id, audio_name=audio_name, video_name=video_name, image_name=image_name)
            db.session.add(post)
            db.session.commit()
            if audio_name != None:
                audio_saver.save(os.path.join(current_app.root_path, "static/audio", audio_name))
            else:
                pass

            if image_name != None:
                image_saver.save(os.path.join(current_app.root_path, "static/images", image_name))
            else:
                pass

            if video_name != None:
                video_saver.save(os.path.join(current_app.root_path, "static/video", video_name))
            else:
                pass

            flash('Post created', category='success')
            return redirect(url_for('views.home'))

    return render_template("create_posts.html", user=current_user)



@views.route("/CreateJournal", methods=['GET', 'POST'])
@login_required
def create_journal():
    if request.method == "POST":
        text = request.form.get('text')
        audio = request.files["audio_journal"]
        video = request.files["video_journal"]
        image = request.files["image_journal"]

        if audio == "<FileStorage: '' ('application/octet-stream')>":
            audio = None

        if video == "<FileStorage: '' ('application/octet-stream')>":
            video = None

        if image == "<FileStorage: '' ('application/octet-stream')>":
            image = None

        #image storage
        image_filename = secure_filename(image.filename)
        print(image_filename)
        if image_filename == '':
            image_name = None
        else:
            image_name = str(uuid.uuid1()) + "_" + image_filename
            print(image_name)

        image_saver = request.files['image_journal']

        #video storage
        video_filename = secure_filename(video.filename)
        print(video_filename)
        if video_filename == '':
            video_name = None
        else:
            video_name = str(uuid.uuid1()) + "_" + video_filename
            print(video_name)

        video_saver = request.files['video_journal']

        #audio storage
        audio_filename = secure_filename(audio.filename)
        print(audio_filename)
        if audio_filename == '':
            audio_name = None
        else:
            audio_name = str(uuid.uuid1()) + "_" + audio_filename
            print(audio_name)

        audio_saver = request.files['audio_journal']

        if not text:
            flash('Post cannot be empty', category='error')
        else:
            post = Journal(text=text, author=current_user.id, audio_name=audio_name, video_name=video_name, image_name=image_name)
            db.session.add(post)
            db.session.commit()
            if audio_name != None:
                audio_saver.save(os.path.join(current_app.root_path, "static/audio", audio_name))
            else:
                pass

            if image_name != None:
                image_saver.save(os.path.join(current_app.root_path, "static/images", image_name))
            else:
                pass

            if video_name != None:
                video_saver.save(os.path.join(current_app.root_path, "static/video", video_name))
            else:
                pass

            flash('Journal created', category='success')
            return redirect(url_for('views.journal_posts', username=current_user.username))

    return render_template("create_journal.html", user=current_user)



@views.route("/delete-post/<id>")
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist", category="error")
    elif current_user.id != post.user.id:
        flash("You do not have permission to delete this post.", category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted', category='success')

    return redirect(url_for('views.posts', username=current_user.username))



@views.route("/delete-journal/<id>")
def delete_journal(id):
    journal = Journal.query.filter_by(id=id).first()

    if not journal:
        flash("Post does not exist", category="error")
    elif current_user.id != journal.user.id:
        flash("You do not have permission to delete this post.", category='error')
    else:
        db.session.delete(journal)
        db.session.commit()
        flash('Journal deleted', category='success')

    return redirect(url_for('views.journal_posts', username=current_user.username))
    


@views.route("/post/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_post(id):
    post_edited = Post.query.get_or_404(id)
    if request.method == "POST":
        edited_post = request.form.get('text')
        
        if edited_post == '':
            post_edited.text = None
        else:
            post_edited.text = edited_post    

        
        if post_edited.text == None:
            flash('The form cannot be empty', category='error')
            return render_template('edit_post.html', user=current_user)
        else:
            db.session.add(post_edited)
            db.session.commit()
            flash("Post has been edited", category='success')

            return redirect(url_for('views.posts', username=post_edited.user.username))

    else:
        return render_template('edit_post.html', user=current_user)



@views.route("/journal/<username>")
@login_required
def journal_posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('Username does not exist', category='error')
        return redirect(url_for('views.home'))

    journals = user.journals
    email = user.email
    
    return render_template("journal.html", user=current_user, journals=journals, username=username, email=email)



@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('Username does not exist', category='error')
        return redirect(url_for('views.home'))

    posts = user.posts
    email = user.email
    profile_pic = user.profile_pic
    return render_template("profile.html", user=current_user, posts=posts, username=username, email=email, profile_pic=profile_pic)



@views.route("/preview")
def PreviewPage():
    posts = Post.query.all()
    return render_template("preview.html", posts=posts)



@views.route('/modal')
def Modal():
    posts = Post.query.all()
    return render_template('GuestModal.html', posts=posts)



class UserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    profile_picture = FileField("Choose profile picture")
    update_field = SubmitField("Update")
    

"""

@views.route('/Update', methods=['GET', 'POST'])
def update():
    username = None
    email = None
    form = UserForm()
    #validate form
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        form.username.data = ''
        form.email.data = ''


    return render_template("UserUpdate.html", username=username, email=email, form=form, user=current_user)

"""
@views.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    form = UserForm()
    username_to_update = User.query.get_or_404(id)
    if request.method == "POST":
        username_to_update.username = request.form["username"]
        username_to_update.email = request.form["email"]
        username_to_update.profile_pic = request.files["profile_picture"]
        if username_to_update.profile_pic == "<FileStorage: '' ('application/octet-stream')>":
            username_to_update.profile_pic = None
        #Saving image name
        pic_filename = secure_filename(username_to_update.profile_pic.filename)
        #set UUID 
        if pic_filename == '':
            picture_name = None
        else:
            picture_name = str(uuid.uuid1()) + "_" + pic_filename

        username_to_update.profile_pic = picture_name
        print(type(pic_filename))
        saver = request.files['profile_picture']

        try:
            db.session.commit()
            #save image
            saver.save(os.path.join(current_app.root_path, "static/images", picture_name))
            

            flash("User updated successfully!")
            return render_template("UserUpdate.html", form=form, username_to_update=username_to_update, user=current_user)
            #saving the image
            

        except:
            flash("Sorry, an issue has occured", category="error")
            return render_template("UserUpdate.html", form=form, username_to_update=username_to_update, user=current_user)

    else:
            return render_template("UserUpdate.html", form=form, username_to_update=username_to_update, user=current_user)
"""

@views.route('/upload', methods=['POST'])
def upload():
    picture = request.files['pic']

    if not picture:
        flash('N')

"""