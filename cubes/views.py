import json
from .models import Cuboid
from django.http import HttpResponse
from .serializers import BoxSerializers
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from Cuboids.settings import A1, V1, L1, L2
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes


#Helper function for creating response
def createResponse(status, message, data=None):
    response = {'status': status,
                'message': message}
    if data is not None:
        response.pop("message")
        response["data"] = data
    return HttpResponse(json.dumps(response), content_type='text/javascript')

#Helper function for Cube Validation Check:
def isValid(Cuboids, length, breadth, height, area, volume, user):
    cuboid_count = Cuboids.count()
    areas = list(Cuboids.values_list("area", flat=True))

    if (sum(areas) + area)/(cuboid_count+1) > A1:
        return createResponse("FAILURE","Average area of a cube shouldn't exceed " + str(A1))

    volumes = list(Cuboids.values_list("volume", flat=True))
    if (sum(volumes) + volume)/(cuboid_count+1) > V1:
        return createResponse("FAILURE",  "Average volume of all Cuboid added shouldn't exceed " + str(V1))

    week = datetime.today() - timedelta(days=7)
    box_week_count = Cuboid.objects.filter(date_of_creation__gte = week).count()
    if box_week_count > L1:
        return createResponse("FAILURE", "Number of the Cubes added in this week has exceeded " + str(L1))

    box_user_week_count = Cuboid.objects.filter(date_of_creation__gte = week, created_by = user).count()
    if box_user_week_count > L2:
        return createResponse("FAILURE", "Number of the Cubes added by You has exceeded " + str(L2))
    return False;
# Add New Users
@csrf_exempt
def addUser(request):
    if request.method == 'POST':
        request_json = json.loads(request.body.decode("utf-8"))
        if 'username'  not in request_json or 'password' not in request_json:
            return createResponse("FAILURE", "Either username or password not present.")
        try:
            # Create user
            User.objects.create_user(**request_json)
            return createResponse("success", 'User Created Successfully')
        except Exception as e:
            return createResponse("FAILURE",str(e))
    return createResponse("FAILURE","Get request is not allowed")

#   Login User and get access token:
@csrf_exempt
def loginUser(request):
    if request.method == 'POST':
        request_json = json.loads(request.body.decode("utf-8"))
        if 'username' not in request_json or 'password' not in request_json:
            return createResponse("FAILURE", "Either username or password not present.")
        username = request_json['username']
        password = request_json['password']
        try:
            user = authenticate(username = username, password = password)  # authenticate that user is exist or not
            if user:
                if user.is_active:
                    login(request, user)
                    token, _ = Token.objects.get_or_create(user=user)
                    data = {'status': 'SUCCESS',
                            'token':token.key,
                            'message': 'Login Successfully'}
                    return HttpResponse(json.dumps(data), content_type='text/javascript')
                else:
                    return createResponse("FAILURE","User is not active")
            else:
                return createResponse("FAILURE", "User does not exists")
        except Exception as d:
            return createResponse("FAILURE",str(d))
    return createResponse("FAILURE", "Not a valid request")

# Add New Cube for the current User:
@csrf_exempt
@api_view(["POST"])
def addCuboid(request):
    if request.user.is_staff:
        global A1, V1, L1, L2
        request_data = json.loads(request.body.decode("utf-8"))
        # Check if all the Three parameters are present or not?
        if "length" not in request_data or "breadth" not in request_data or "height" not in request_data:
            return createResponse("FAILURE", "Length , Breadth and Height must be in parameters!")
        length = request_data["length"]
        breadth = request_data["breadth"]
        height = request_data["height"]
        area = 2 * (length * breadth + breadth * height + height * length)
        volume = length * breadth * height
        Cuboids = Cuboid.objects.all()
        # Check if Conditions for adding the Cube is Valid or Not? If not return with message:
        if Cuboids.count() != 0:
            res = isValid(Cuboids, length, breadth, height, area, volume, request.user)
            if(res):
                return res
        # Add the Cube to the Database as it passed all requirements:
        Cuboid.objects.create(length=length, breadth=breadth, height=height, area=area, volume=volume, created_by=request.user)
        return createResponse("SUCCESS","Cube is added successfully.")
    else:
        # If the User is not a Staff member:
        return createResponse("FAILURE", "You don't have permission to add the Cube.")

# Update Existing Cube with a particular ID:
@csrf_exempt
@api_view(["PUT"])
def updateCuboid(request):
    if request.user.is_staff:
        global A1,V1
        request_data = json.loads(request.body.decode("utf-8"))
        if "id" not in request_data or request_data["id"] == "":
            return createResponse("FAILURE", "Either id is null or id is not present")
        if Cuboid.objects.filter(id = request_data["id"]).exists():
            cuboid = Cuboid.objects.get(id=request_data["id"])
            if "length" not in request_data:
                length = cuboid.length
            else:
                length = request_data["length"]
            if "breadth" not in request_data:
                breadth = cuboid.breadth
            else:
                breadth = request_data["breadth"]
            if "height" not in request_data:
                height  = cuboid.height
            else:
                height = request_data["height"]

            area = 2*( length * breadth + breadth * height + height * length )
            volume = length * breadth * height
            boxes = Cuboid.objects.all()
            boxes = boxes.exclude(id = request_data['id'])
            box_count = boxes.count()

            areas = list(boxes.values_list("area", flat=True))
            if (sum(areas) + area) / (box_count + 1) > A1:
                return createResponse("FAILURE","Average area of the boxes shouldn't exceed " + str(A1))

            volumes = list(boxes.values_list("volume", flat=True))
            if (sum(volumes) + volume) / (box_count + 1) > V1:
                return createResponse("FAILURE","Average volume of the boxes shouldn't exceed " + str(V1))
            cuboid.length = length
            cuboid.breadth = breadth
            cuboid.height = height
            cuboid.area = area
            cuboid.volume = volume
            cuboid.save()
            return createResponse("SUCCESS", "Box is Updated successfully.")
        else:
            return createResponse("FAILURE", "Box with given id is not exist.")
    else:
        return createResponse("FAILURE", "You haven't permission to update the box.")

# Delete Cube with a Given ID:
@csrf_exempt
@api_view(["POST"])
def deleteCuboid(request):
    if request.user.is_staff:
        request_data = json.loads(request.body.decode("utf-8"))
        #if user doesn't send the id by mistake
        if "id" not in request_data or request_data["id"] == "":
            return createResponse("FAILURE", "Either id is null or id is not present")
        if Cuboid.objects.filter(id=request_data["id"]).exists():
            box  = Cuboid.objects.get(id = request_data["id"])
            # If the user is not the Creator of the Box:
            if request.user != box.created_by:
                return createResponse("FAILURE", "Only creator of Cube can delete the Cube.")

            box.delete()
            return createResponse("SUCCESS", "Cube is deleted successfully.")
        else:
            # If Cube with the Given Id doesn't Exists:
            return createResponse("FAILURE", "Cube with given id is not exist.")
    else:
        # If the User is not a Staff member:
        return createResponse("FAILURE", "You haven't permission to delete the Cube")


# This function will help in filtering the data on the basis of the filter applied by the user
# And if we pass the user then it will return the box created by the user
def filterFunction(filters, request, user = None):
    filter_query = {}
    # Making the query dict for filtering
    for params in filters:
        # Converting the string date time into python date
        if params == "date_of_creation":
            date = datetime.strptime(filters[params]["value"], "%d/%m/%Y").strftime("%Y-%m-%d")
            filter_query[params + "__" + filters[params]["condition"]] = date
        # So only allbox api will use this not the my box api where box will already filterd on the basis of username
        elif params == "created_by" and user is None:
            filter_query["created_by__username"] = filters[params]
        else:
            filter_query[params + "__" + filters[params]["condition"]] = filters[params]["value"]
    # For my Cube api
    if user is not None:
        filter_query["created_by"] = user
    Cubes = Cuboid.objects.filter(**filter_query)
    filtered_Cube = BoxSerializers(Cubes,many=True, context={"request":request})
    return filtered_Cube.data

# Get all the Cubes from the DataBase:
@csrf_exempt
@api_view(["GET"])
@permission_classes([AllowAny])
def getAllCuboids(request):
    filter_data = json.loads(request.body.decode("utf-8"))
    return createResponse("SUCCESS", "",filterFunction(filter_data["filters"],request))


# Get All the Cubes Created By the Current User:
@csrf_exempt
@api_view(["GET"])
def getMyCuboids(request):
    if request.user.is_staff:
        filter_data = json.loads(request.body.decode("utf-8"))
        return createResponse("SUCCESS", "", filterFunction(filter_data["filters"], request, request.user))
    else:
        # If the User is not a Staff member:
        return createResponse("FAILURE", "Valid Only for Staff and LoggedIn Users!")