from app import app, db

from flask import request, jsonify

from models import Friend


# Get all friends

@app.route('/api/friends', methods=['GET'])

def get_friends():
    friends = Friend.query.all()
    result = [friend.to_json() for friend in friends]

    return jsonify(result)


# Create a new friend

@app.route('/api/friends', methods=["POST"])

def create_friend():
    try:
        data = request.json

        required_fields = ["name", "role", "description", "gender"]

        for field in required_fields:
            if not data.get(field) or field not in data:
                return jsonify({"error": f"Field {field} is required"}), 400

        name = data.get("name")
        role = data.get("role")
        description = data.get("description")
        gender = data.get("gender")


        # fetch avatar image based on gender
        if gender == "male":
            img_url = f"https://avatar.iran.liara.run/public/boy?username={name}"
        else:
            img_url = f"https://avatar.iran.liara.run/public/girl?username={name}"

        new_friend = Friend(name=name, role=role, description=description,gender=gender, img_url=img_url)
        db.session.add(new_friend)
        db.session.commit()

        return jsonify(new_friend.to_json()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Delete a friend by id


@app.route('/api/friends/<int:friend_id>', methods=["DELETE"])

def delete_friend(friend_id):
    try:
        friend = Friend.query.get(friend_id)
        if friend is None:
            return jsonify({"error": "Friend not found"}), 404
        db.session.delete(friend)
        db.session.commit()

        return jsonify(friend.to_json()), 200
    

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Update a Friend by id 

@app.route('/api/friends/<int:friend_id>', methods=["PATCH"])

def update_friend(friend_id):
    try:
        friend = Friend.query.get(friend_id)
        if friend is None:
            return jsonify({"error": "Friend not found"}), 404
        data = request.json
        for field in data:
            setattr(friend, field, data[field])
            
        db.session.commit()

        return jsonify( friend.to_json()), 200
    

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500