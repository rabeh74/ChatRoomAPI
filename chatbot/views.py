def room(request, username, room_name):
    return render(request, 'chatbot/room.html', {
        'room_name': room_name,
        'username': username
    }) 