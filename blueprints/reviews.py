from flask import Blueprint, render_template, request, redirect, session
from db import insert_travel_log ,insert_spot ,insert_image ,select_from_table ,get_travel_logs_by_user
import os
from werkzeug.utils import secure_filename

reviews_bp = Blueprint('reviews', __name__, url_prefix='/reviews')

@reviews_bp.route('/')
def reviews():
    if 'user_id' not in session:
        return redirect('/auth/login')
    user_id = session['user_id']
    travel_logs = get_travel_logs_by_user(user_id)
    return render_template('reviews.html', travel_logs=travel_logs)

@reviews_bp.route('/add', methods=['GET', 'POST'])
def add_review():
    if 'user_id' not in session:
        return redirect('/auth/login')


    if request.method == 'POST':
        user_id = session['user_id']
        trip_title = request.form['trip_title']
        itinerary_count = int(request.form['itinerary_count'])

        # 旅ログを登録
        insert_travel_log(trip_title, user_id)
        log_id = select_from_table("travei_log", f"title = '{trip_title}'")[0]
        print(log_id)
        # スポットと画像を登録
        for i in range(1, itinerary_count + 1):
            access_rating = request.form.get(f'access_rating_{i}')
            experience_rating = request.form.get(f'experience_rating_{i}')
            price_rating = request.form.get(f'price_rating_{i}')
            location = request.form.get(f'location_{i}')
        if location:
            latitude, longitude = map(float, location.split(', '))
        else:
            # 位置情報が空の場合のデフォルト値またはエラーハンドリング
            latitude, longitude = None, None  # または適切なデフォルト値

            print(insert_spot(log_id, i, user_id, access_rating, experience_rating, price_rating, latitude, longitude))
            images = request.files.getlist(f'images_{i}')
            for index, image in enumerate(images):
                if image and '.' in image.filename:
                    filename = secure_filename(image.filename)
                    filepath = os.path.join('static/uploads', filename)
                    image.save(filepath)

                    insert_image(filepath, user_id, log_id, i, index + 1)

        return redirect('/profile')

    return render_template('add.html')

@reviews_bp.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/auth/login')
    user_id = session['user_id']
    travel_logs = get_travel_logs_by_user(user_id)
    return render_template('profile.html', travel_logs=travel_logs)

