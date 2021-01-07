if ObjectId(character_id) in favourite_characters:
            flash("Already in favourites")
            return redirect(url_for("characters"))
        profile = mongo.db.users.find_one(
            {'username': session["user"].lower()})
        mongo.db.users.update_one(
            profile, {"$push": {"favourites": ObjectId(character_id)}})
        flash("Character added to Favourites")
        return redirect(url_for('characters'))