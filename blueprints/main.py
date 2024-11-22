from flask import Blueprint, render_template
from db import *

main_bp = Blueprint('main', __name__, url_prefix='/')

@main_bp.route('/')
def index():
    images = select_from_table('images')
    print(images)
    # for i in images:
    #     images[i](7) = select_from_table('users', images(i[2]))
    #     images[i](8) = select_from_table('travel_logs', images(i[3]))

    # images = [(1, 'static/uploads/e_1114.png', 2, 1, 4, 5)]

    # 6つ目の項目を追加（例: "new_item" を追加）
    for i in range(len(images)):
        images = [image + (f"{select_from_table('user',user_id = image[i](2))}",) for image in images]
    print(images)

    response = images
    print(response)
    return render_template('index.html', images=response)