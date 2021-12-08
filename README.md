# How to use:
- Create a virtual environment with the python version should 3.10.0.
- Extract the zip file of the projects
- Activate the virtual environment and run the following command:
    * pip install -r requirements.txt
- Add the token into header

## Start Server:
    python manage.py runserver

## CRUD-API End Points:
- Add User:
    * http://127.0.0.1:8000/api/addUser/
- User Login:
    * http://127.0.0.1:8000/api/userLogin/
- Add Cube:
    * http://127.0.0.1:8000/api/addCuboid/
- Update Cube:
    * http://127.0.0.1:8000/api/updateCuboid/
- List all Cubes:
    * http://127.0.0.1:8000/api/getAllCuboids/
- List My Cubes: 
    * http://127.0.0.1:8000/api/getMyCuboids/
- Delete Cube:
    * http://127.0.0.1:8000/api/deleteCuboid/
    
## Problem Description:
- Consider a store which has an inventory of boxes which are all cuboid(which have length breadth and height). Each Cuboid has been added by a store employee who is associated as the creator of the box even if it is updated by any user later on.

## Tasks:
- Data Modelling:
    * Build minimal Models required for the such a store. You can use contrib modules for necessary models(for eg: users)

- ##  Build api for the following specifications:
    - ### Add Cube API
    - ### Update Cube API
    - ### List All API
    - ### List My Cubes
    - ### Delete Cube API
        
- ### Conditions to be fulfilled on each add/update/delete:
    - Average area of all added boxes should not exceed A1
    - Average volume of all boxes added by the current user shall not exceed V1
    - Total Boxes added in a week cannot be more than L1
    - Total Boxes added in a week by a user cannot be more than L2

- #### Values A1, V1, L1 and L2 shall be configured externally. You can choose 100, 1000, 100, and 50 as their respective default values.
