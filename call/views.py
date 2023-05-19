from django.shortcuts import render
from django.http import JsonResponse
import random
import time
from agora_token_builder import RtcTokenBuilder
from .models import RoomMember
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required



# Create your views here.
@login_required
def lobby(request):
    context = {
        "title": "SpectaX-Join the Chat!",
    }
    return render(request, 'call/lobby.html', context)
@login_required
def room(request):
    context = {
        "title": "SpectaX-Video Chat"
    }
    return render(request, 'call/room.html', context)


def getToken(request):
    appId = "3b8715d70eb24308b4bb45a28bce1249"
    appCertificate = "e951e6d88a184ab79e481485ca7aa147"
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid}, safe=False)


@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )

    return JsonResponse({'name':data['name']}, safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name':member.name}, safe=False)

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    print("member name", member)
    member.delete()
    return JsonResponse('Member deleted', safe=False)

def upload_image(request):
    if request.method == 'POST':
        image_data = request.POST.get('image')
        image_data = image_data.replace('data:image/png;base64,', '')  # remove the data URI scheme prefix
        image_bytes = base64.b64decode(image_data)
        
        # save the image to a file
        # with open('image.png', 'wb') as f:
        #     f.write(image_bytes)

        print('image recieved')
        
        # or save the image to a database using Django's ORM
        # ...

        return JsonResponse({'message': 'Image uploaded successfully.'})
    else:
        return JsonResponse({'message': 'Only POST requests are allowed.'}, status=405)