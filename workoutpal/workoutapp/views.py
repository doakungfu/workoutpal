from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, 'workouts/index.html')

def register(request):
    errors = User.objects.register_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        )
        request.session['user_id'] = user.id
        request.session['greeting'] = user.first_name
        return redirect('/workouts')

def login(request):
    errors = User.objects.login_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['login_email'])
        request.session['user_id'] = user.id
        request.session['greeting'] = user.first_name
        return redirect('/workouts')

def show_all(request):
    # check to see if the user loggedin or registered by checking their session
    if "user_id" not in request.session:
        return redirect('/')
    else:
        context = {
            'all_workouts': Workout.objects.all(),
            'this_user': User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'workouts/show_all.html', context)

def create_workout(request):
    errors = Workout.objects.workout_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/workouts')
    else:
        user = User.objects.get(id=request.session["user_id"])
        workout = Workout.objects.create(
            title = request.POST['title'],
            description = request.POST['description'],
            creator = user
        )
        # bonus: the workout creator automatically favorites the workout
        user.favorited_workouts.add(workout)

        return redirect(f'/workouts/{workout.id}')

def show_one(request, workout_id):
    context = {
        'workout': Workout.objects.get(id=workout_id),
        'current_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, "workouts/show_one.html", context)

def update(request, workout_id):
    workout = Workout.objects.get(id=workout_id)
    workout.description = request.POST['description']
    workout.save()

    return redirect(f"/workouts/{workout_id}")

def delete(request, workout_id):
    workout = Workout.objects.get(id=workout_id)
    workout.delete()

    return redirect('/workouts')

def favorite(request, workout_id):
    user = User.objects.get(id=request.session["user_id"])
    workout = Workout.objects.get(id=workout_id)
    user.favorited_workouts.add(workout)

    return redirect(f'/workouts/{workout_id}')

def unfavorite(request, workout_id):
    user = User.objects.get(id=request.session["user_id"])
    workout = Workout.objects.get(id=workout_id)
    user.favorited_workouts.remove(workout)

    return redirect(f'/workouts/{workout_id}')

def logout(request):
    request.session.flush()

    return redirect('/')