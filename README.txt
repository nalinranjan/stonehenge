CSCI 610 - Foundations of Computer Graphics
Final Project
By: Nalin Ranjan

The scene depicts a simplified interpretation of Stonehenge.

--------------------
DEVELOPMENT PLATFORM
--------------------
    Language                 :  Python 3.6.3 (64-bit)
    Operating System         :  Windows 10 (64-bit)
    Supported OpenGL Version :  4.4

    OpenGL Version Used      :  3.2
    GLSL Version Used        :  1.5

--------------
FILES INCLUDED
--------------
    Python source
        - boulder.py
        - camera.py
        - ground.py
        - light.py
        - object.py
        - pysoil.py
        - scene.py
        - stone.py
    
    GLSL
        - ground_shader.frag
        - ground_shader.vert
        - stone_shader.frag
        - stone_shader.vert
    
    grass_texture.jpg
    README.txt

------------
INSTRUCTIONS
------------
    The submission includes a modified version of pysoil.py which makes some
    changes for Python 3.x compatibility. The official pysoil implementation
    only supports Python 2.x. The modified version needs to be used to run this
    code. It also needs the modified soil.dll that was uploaded to myCourses.

    To run the code, place all supplied files in the same directory. With this
    directory as the current working directory, run scene.py with Python 3. 

        python scene.py

    Once the window is rendered, use the 'a' and 'd' keys to rotate the scene
    clockwise and counter-clockwise respectively.

------------
ATTRIBUTIONS
------------
    pysoil - Python wrapper for the SOIL C library used to load textures
    OpenGL.org Discussion Board - For help with texture rendering problems
    Scratchapixel.com - For help with understanding the perspective projection matrix