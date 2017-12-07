# Copyright(c) Max Kolosov 2010 maxkolosov@inbox.ru
# http://vosolok2008.narod.ru
# BSD license

__version__ = '0.1'
__versionTime__ = '2010-02-12'
__author__ = 'Max Kolosov <maxkolosov@inbox.ru>'
__doc__ = '''
pysoil.py - is ctypes python module for
SOIL - Simple OpenGL Image Library (http://www.lonesock.net).
A tiny c library for uploading images as textures into OpenGL.
Also saving and loading of images is supported.

Image Formats:
- BMP		load & save
- TGA		load & save
- DDS		load & save
- PNG		load
- JPG		load

OpenGL Texture Features:
- resample to power-of-two sizes
- MIPmap generation
- compressed texture S3TC formats (if supported)
- can pre-multiply alpha for you, for better compositing
- can flip image about the y-axis (except pre-compressed DDS files)
'''

import sys, ctypes, platform

c_int_p = ctypes.POINTER(ctypes.c_int)
c_uchar_p = ctypes.POINTER(ctypes.c_ubyte)

if platform.system().lower() == 'windows':
    soil_module = ctypes.WinDLL('soil')
    func_type = ctypes.WINFUNCTYPE
else:
    soil_module = ctypes.CDLL('soil')
    func_type = ctypes.CFUNCTYPE


# The format of images that may be loaded (force_channels).
SOIL_LOAD_AUTO = 0# SOIL_LOAD_AUTO leaves the image in whatever format it was found.
SOIL_LOAD_L = 1# SOIL_LOAD_L forces the image to load as Luminous (greyscale)
SOIL_LOAD_LA = 2# SOIL_LOAD_LA forces the image to load as Luminous with Alpha
SOIL_LOAD_RGB = 3# SOIL_LOAD_RGB forces the image to load as Red Green Blue
SOIL_LOAD_RGBA = 4# SOIL_LOAD_RGBA forces the image to load as Red Green Blue Alpha

# Passed in as reuse_texture_ID, will cause SOIL to
# register a new texture ID using glGenTextures().
# If the value passed into reuse_texture_ID > 0 then
# SOIL will just re-use that texture ID (great for
# reloading image assets in-game!)
SOIL_CREATE_NEW_ID = 0

# flags you can pass into SOIL_load_OGL_texture()
# and SOIL_create_OGL_texture().
# (note that if SOIL_FLAG_DDS_LOAD_DIRECT is used
# the rest of the flags with the exception of
# SOIL_FLAG_TEXTURE_REPEATS will be ignored while
# loading already-compressed DDS files.)
SOIL_FLAG_POWER_OF_TWO = 1# SOIL_FLAG_POWER_OF_TWO: force the image to be POT
SOIL_FLAG_MIPMAPS = 2# SOIL_FLAG_MIPMAPS: generate mipmaps for the texture
SOIL_FLAG_TEXTURE_REPEATS = 4# SOIL_FLAG_TEXTURE_REPEATS: otherwise will clamp
SOIL_FLAG_MULTIPLY_ALPHA = 8# SOIL_FLAG_MULTIPLY_ALPHA: for using (GL_ONE,GL_ONE_MINUS_SRC_ALPHA) blending
SOIL_FLAG_INVERT_Y = 16# SOIL_FLAG_INVERT_Y: flip the image vertically
SOIL_FLAG_COMPRESS_TO_DXT = 32# SOIL_FLAG_COMPRESS_TO_DXT: if the card can display them, will convert RGB to DXT1, RGBA to DXT5
SOIL_FLAG_DDS_LOAD_DIRECT = 64# SOIL_FLAG_DDS_LOAD_DIRECT: will load DDS files directly without _ANY_ additional processing
SOIL_FLAG_NTSC_SAFE_RGB = 128# SOIL_FLAG_NTSC_SAFE_RGB: clamps RGB components to the range [16,235]
SOIL_FLAG_CoCg_Y = 256# SOIL_FLAG_CoCg_Y: Google YCoCg; RGB=>CoYCg, RGBA=>CoCgAY
SOIL_FLAG_TEXTURE_RECTANGLE = 512# SOIL_FLAG_TEXTURE_RECTANGE: uses ARB_texture_rectangle ; pixel indexed & no repeat or MIPmaps or cubemaps

# The types of images that may be saved.
SOIL_SAVE_TYPE_TGA = 0# (TGA supports uncompressed RGB / RGBA)
SOIL_SAVE_TYPE_BMP = 1# (BMP supports uncompressed RGB)
SOIL_SAVE_TYPE_DDS = 2# (DDS supports DXT1 and DXT5)

# Defines the order of faces in a DDS cubemap.
# I recommend that you use the same order in single
# image cubemap files, so they will be interchangeable
# with DDS cubemaps when using SOIL.
SOIL_DDS_CUBEMAP_FACE_ORDER = b'EWUDNS'
#~ SOIL_DDS_CUBEMAP_FACE_ORDER = (ctypes.c_char * 6)('E','W','U','D','N','S')

# The types of internal fake HDR representations
SOIL_HDR_RGBE = 0# SOIL_HDR_RGBE:		RGB * pow( 2.0, A - 128.0 )
SOIL_HDR_RGBdivA = 1# SOIL_HDR_RGBdivA:	RGB / A
SOIL_HDR_RGBdivA2 = 2# SOIL_HDR_RGBdivA2:	RGB / (A*A)

# Loads an image from disk into an OpenGL texture.
# \param filename the name of the file to upload as a texture
# \param force_channels 0-image format, 1-luminous, 2-luminous/alpha, 3-RGB, 4-RGBA
# \param reuse_texture_ID 0-generate a new texture ID, otherwise reuse the texture ID (overwriting the old texture)
# \param flags can be any of SOIL_FLAG_POWER_OF_TWO | SOIL_FLAG_MIPMAPS | SOIL_FLAG_TEXTURE_REPEATS | SOIL_FLAG_MULTIPLY_ALPHA | SOIL_FLAG_INVERT_Y | SOIL_FLAG_COMPRESS_TO_DXT | SOIL_FLAG_DDS_LOAD_DIRECT
# \return 0-failed, otherwise returns the OpenGL texture handle
#unsigned int SOIL_load_OGL_texture (const char *filename, int force_channels, unsigned int reuse_texture_ID, unsigned int flags);
SOIL_load_OGL_texture = func_type(ctypes.c_uint, ctypes.c_char_p, ctypes.c_int, ctypes.c_uint, ctypes.c_uint)(('SOIL_load_OGL_texture', soil_module))

# Loads 6 images from disk into an OpenGL cubemap texture.
# \param x_pos_file the name of the file to upload as the +x cube face
# \param x_neg_file the name of the file to upload as the -x cube face
# \param y_pos_file the name of the file to upload as the +y cube face
# \param y_neg_file the name of the file to upload as the -y cube face
# \param z_pos_file the name of the file to upload as the +z cube face
# \param z_neg_file the name of the file to upload as the -z cube face
# \param force_channels 0-image format, 1-luminous, 2-luminous/alpha, 3-RGB, 4-RGBA
# \param reuse_texture_ID 0-generate a new texture ID, otherwise reuse the texture ID (overwriting the old texture)
# \param flags can be any of SOIL_FLAG_POWER_OF_TWO | SOIL_FLAG_MIPMAPS | SOIL_FLAG_TEXTURE_REPEATS | SOIL_FLAG_MULTIPLY_ALPHA | SOIL_FLAG_INVERT_Y | SOIL_FLAG_COMPRESS_TO_DXT | SOIL_FLAG_DDS_LOAD_DIRECT
# \return 0-failed, otherwise returns the OpenGL texture handle
# unsigned int SOIL_load_OGL_cubemap (const char *x_pos_file, const char *x_neg_file, const char *y_pos_file, const char *y_neg_file, const char *z_pos_file, const char *z_neg_file, int force_channels, unsigned int reuse_texture_ID, unsigned int flags);
SOIL_load_OGL_cubemap = func_type(ctypes.c_uint, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_uint, ctypes.c_uint)(('SOIL_load_OGL_cubemap', soil_module))

# Loads 1 image from disk and splits it into an OpenGL cubemap texture.
# \param filename the name of the file to upload as a texture
# \param face_order the order of the faces in the file, any combination of NSWEUD, for North, South, Up, etc.
# \param force_channels 0-image format, 1-luminous, 2-luminous/alpha, 3-RGB, 4-RGBA
# \param reuse_texture_ID 0-generate a new texture ID, otherwise reuse the texture ID (overwriting the old texture)
# \param flags can be any of SOIL_FLAG_POWER_OF_TWO | SOIL_FLAG_MIPMAPS | SOIL_FLAG_TEXTURE_REPEATS | SOIL_FLAG_MULTIPLY_ALPHA | SOIL_FLAG_INVERT_Y | SOIL_FLAG_COMPRESS_TO_DXT | SOIL_FLAG_DDS_LOAD_DIRECT
# \return 0-failed, otherwise returns the OpenGL texture handle
# unsigned int SOIL_load_OGL_single_cubemap (const char *filename, const char face_order[6], int force_channels, unsigned int reuse_texture_ID, unsigned int flags);
SOIL_load_OGL_single_cubemap = func_type(ctypes.c_uint, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_uint, ctypes.c_uint)(('SOIL_load_OGL_single_cubemap', soil_module))
#~ SOIL_load_OGL_single_cubemap = func_type(ctypes.c_uint, ctypes.c_char_p, ctypes.c_char*6, ctypes.c_int, ctypes.c_uint, ctypes.c_uint)(('SOIL_load_OGL_single_cubemap', soil_module))

# Loads an HDR image from disk into an OpenGL texture.
# \param filename the name of the file to upload as a texture
# \param fake_HDR_format SOIL_HDR_RGBE, SOIL_HDR_RGBdivA, SOIL_HDR_RGBdivA2
# \param reuse_texture_ID 0-generate a new texture ID, otherwise reuse the texture ID (overwriting the old texture)
# \param flags can be any of SOIL_FLAG_POWER_OF_TWO | SOIL_FLAG_MIPMAPS | SOIL_FLAG_TEXTURE_REPEATS | SOIL_FLAG_MULTIPLY_ALPHA | SOIL_FLAG_INVERT_Y | SOIL_FLAG_COMPRESS_TO_DXT
# \return 0-failed, otherwise returns the OpenGL texture handle
# unsigned int SOIL_load_OGL_HDR_texture (const char *filename, int fake_HDR_format, int rescale_to_max, unsigned int reuse_texture_ID, unsigned int flags);
SOIL_load_OGL_HDR_texture = func_type(ctypes.c_uint, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.c_uint)(('SOIL_load_OGL_HDR_texture', soil_module))

# Loads an image from RAM into an OpenGL texture.
# \param buffer the image data in RAM just as if it were still in a file
# \param buffer_length the size of the buffer in bytes
# \param force_channels 0-image format, 1-luminous, 2-luminous/alpha, 3-RGB, 4-RGBA
# \param reuse_texture_ID 0-generate a new texture ID, otherwise reuse the texture ID (overwriting the old texture)
# \param flags can be any of SOIL_FLAG_POWER_OF_TWO | SOIL_FLAG_MIPMAPS | SOIL_FLAG_TEXTURE_REPEATS | SOIL_FLAG_MULTIPLY_ALPHA | SOIL_FLAG_INVERT_Y | SOIL_FLAG_COMPRESS_TO_DXT | SOIL_FLAG_DDS_LOAD_DIRECT
# \return 0-failed, otherwise returns the OpenGL texture handle
# unsigned int SOIL_load_OGL_texture_from_memory (const unsigned char *const buffer, int buffer_length, int force_channels, unsigned int reuse_texture_ID, unsigned int flags);
SOIL_load_OGL_texture_from_memory = func_type(ctypes.c_uint, c_uchar_p, ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.c_uint)(('SOIL_load_OGL_texture_from_memory', soil_module))

# Loads 6 images from memory into an OpenGL cubemap texture.
# \param x_pos_buffer the image data in RAM to upload as the +x cube face
# \param x_pos_buffer_length the size of the above buffer
# \param x_neg_buffer the image data in RAM to upload as the +x cube face
# \param x_neg_buffer_length the size of the above buffer
# \param y_pos_buffer the image data in RAM to upload as the +x cube face
# \param y_pos_buffer_length the size of the above buffer
# \param y_neg_buffer the image data in RAM to upload as the +x cube face
# \param y_neg_buffer_length the size of the above buffer
# \param z_pos_buffer the image data in RAM to upload as the +x cube face
# \param z_pos_buffer_length the size of the above buffer
# \param z_neg_buffer the image data in RAM to upload as the +x cube face
# \param z_neg_buffer_length the size of the above buffer
# \param force_channels 0-image format, 1-luminous, 2-luminous/alpha, 3-RGB, 4-RGBA
# \param reuse_texture_ID 0-generate a new texture ID, otherwise reuse the texture ID (overwriting the old texture)
# \param flags can be any of SOIL_FLAG_POWER_OF_TWO | SOIL_FLAG_MIPMAPS | SOIL_FLAG_TEXTURE_REPEATS | SOIL_FLAG_MULTIPLY_ALPHA | SOIL_FLAG_INVERT_Y | SOIL_FLAG_COMPRESS_TO_DXT | SOIL_FLAG_DDS_LOAD_DIRECT
# \return 0-failed, otherwise returns the OpenGL texture handle
# unsigned int SOIL_load_OGL_cubemap_from_memory (const unsigned char *const x_pos_buffer, int x_pos_buffer_length, const unsigned char *const x_neg_buffer, int x_neg_buffer_length, const unsigned char *const y_pos_buffer, int y_pos_buffer_length, const unsigned char *const y_neg_buffer, int y_neg_buffer_length, const unsigned char *const z_pos_buffer, int z_pos_buffer_length, const unsigned char *const z_neg_buffer, int z_neg_buffer_length, int force_channels, unsigned int reuse_texture_ID, unsigned int flags);
SOIL_load_OGL_cubemap_from_memory = func_type(ctypes.c_uint, c_uchar_p, ctypes.c_int, c_uchar_p, ctypes.c_int, c_uchar_p, ctypes.c_int, c_uchar_p, ctypes.c_int, c_uchar_p, ctypes.c_int, c_uchar_p, ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.c_uint)(('SOIL_load_OGL_cubemap_from_memory', soil_module))

# Loads 1 image from RAM and splits it into an OpenGL cubemap texture.
# \param buffer the image data in RAM just as if it were still in a file
# \param buffer_length the size of the buffer in bytes
# \param face_order the order of the faces in the file, any combination of NSWEUD, for North, South, Up, etc.
# \param force_channels 0-image format, 1-luminous, 2-luminous/alpha, 3-RGB, 4-RGBA
# \param reuse_texture_ID 0-generate a new texture ID, otherwise reuse the texture ID (overwriting the old texture)
# \param flags can be any of SOIL_FLAG_POWER_OF_TWO | SOIL_FLAG_MIPMAPS | SOIL_FLAG_TEXTURE_REPEATS | SOIL_FLAG_MULTIPLY_ALPHA | SOIL_FLAG_INVERT_Y | SOIL_FLAG_COMPRESS_TO_DXT | SOIL_FLAG_DDS_LOAD_DIRECT
# \return 0-failed, otherwise returns the OpenGL texture handle
# unsigned int SOIL_load_OGL_single_cubemap_from_memory (const unsigned char *const buffer, int buffer_length, const char face_order[6], int force_channels, unsigned int reuse_texture_ID, unsigned int flags);
SOIL_load_OGL_single_cubemap_from_memory = func_type(ctypes.c_uint, c_uchar_p, ctypes.c_int, ctypes.c_char*6, ctypes.c_int, ctypes.c_uint, ctypes.c_uint)(('SOIL_load_OGL_single_cubemap_from_memory', soil_module))

# Creates a 2D OpenGL texture from raw image data.  Note that the raw data is
# _NOT_ freed after the upload (so the user can load various versions).
# \param data the raw data to be uploaded as an OpenGL texture
# \param width the width of the image in pixels
# \param height the height of the image in pixels
# \param channels the number of channels: 1-luminous, 2-luminous/alpha, 3-RGB, 4-RGBA
# \param reuse_texture_ID 0-generate a new texture ID, otherwise reuse the texture ID (overwriting the old texture)
# \param flags can be any of SOIL_FLAG_POWER_OF_TWO | SOIL_FLAG_MIPMAPS | SOIL_FLAG_TEXTURE_REPEATS | SOIL_FLAG_MULTIPLY_ALPHA | SOIL_FLAG_INVERT_Y | SOIL_FLAG_COMPRESS_TO_DXT
# \return 0-failed, otherwise returns the OpenGL texture handle
# unsigned int SOIL_create_OGL_texture (const unsigned char *const data, int width, int height, int channels, unsigned int reuse_texture_ID, unsigned int flags);
SOIL_create_OGL_texture = func_type(ctypes.c_uint, c_uchar_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.c_uint)(('SOIL_create_OGL_texture', soil_module))

# Creates an OpenGL cubemap texture by splitting up 1 image into 6 parts.
# \param data the raw data to be uploaded as an OpenGL texture
# \param width the width of the image in pixels
# \param height the height of the image in pixels
# \param channels the number of channels: 1-luminous, 2-luminous/alpha, 3-RGB, 4-RGBA
# \param face_order the order of the faces in the file, and combination of NSWEUD, for North, South, Up, etc.
# \param reuse_texture_ID 0-generate a new texture ID, otherwise reuse the texture ID (overwriting the old texture)
# \param flags can be any of SOIL_FLAG_POWER_OF_TWO | SOIL_FLAG_MIPMAPS | SOIL_FLAG_TEXTURE_REPEATS | SOIL_FLAG_MULTIPLY_ALPHA | SOIL_FLAG_INVERT_Y | SOIL_FLAG_COMPRESS_TO_DXT | SOIL_FLAG_DDS_LOAD_DIRECT
# \return 0-failed, otherwise returns the OpenGL texture handle
# unsigned int SOIL_create_OGL_single_cubemap (const unsigned char *const data, int width, int height, int channels, const char face_order[6], unsigned int reuse_texture_ID, unsigned int flags);
SOIL_create_OGL_single_cubemap = func_type(ctypes.c_uint, c_uchar_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char*6, ctypes.c_uint, ctypes.c_uint)(('SOIL_create_OGL_single_cubemap', soil_module))

# Captures the OpenGL window (RGB) and saves it to disk
# \return 0 if it failed, otherwise returns 1
# int SOIL_save_screenshot (const char *filename, int image_type, int x, int y, int width, int height);
SOIL_save_screenshot = func_type(ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)(('SOIL_save_screenshot', soil_module))

# Loads an image from disk into an array of unsigned chars.
# Note that *channels return the original channel count of the
# image.  If force_channels was other than SOIL_LOAD_AUTO,
# the resulting image has force_channels, but *channels may be
# different (if the original image had a different channel
# count).
# unsigned char* SOIL_load_image (const char *filename, int *width, int *height, int *channels, int force_channels);
SOIL_load_image = func_type(c_uchar_p, ctypes.c_char_p, c_int_p, c_int_p, c_int_p, ctypes.c_int)(('SOIL_load_image', soil_module))

# Loads an image from memory into an array of unsigned chars.
# Note that *channels return the original channel count of the
# image.  If force_channels was other than SOIL_LOAD_AUTO,
# the resulting image has force_channels, but *channels may be
# different (if the original image had a different channel
# count).
# unsigned char* SOIL_load_image_from_memory (const unsigned char *const buffer, int buffer_length, int *width, int *height, int *channels, int force_channels);
SOIL_load_image_from_memory = func_type(c_uchar_p, c_uchar_p, ctypes.c_int, c_int_p, c_int_p, c_int_p, ctypes.c_int)(('SOIL_load_image_from_memory', soil_module))

# Saves an image from an array of unsigned chars (RGBA) to disk
# \return 0 if failed, otherwise returns 1
# int SOIL_save_image (const char *filename, int image_type, int width, int height, int channels, const unsigned char *const data);
SOIL_save_image = func_type(ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, c_uchar_p)(('SOIL_save_image', soil_module))

# Frees the image data (note, this is just C's "free()"...this function is
# present mostly so C++ programmers don't forget to use "free()" and call
# "delete []" instead [8^)
# void SOIL_free_image_data (unsigned char *img_data);
SOIL_free_image_data = func_type(None, c_uchar_p)(('SOIL_free_image_data', soil_module))

# This function resturn a pointer to a string describing the last thing
# that happened inside SOIL.  It can be used to determine why an image
# failed to load.
# const char* SOIL_last_result (void);
SOIL_last_result = func_type(ctypes.c_char_p)(('SOIL_last_result', soil_module))


if __name__ == "__main__":
    import time
    from OpenGL.GL import *
    from OpenGL.GLUT import *
    from OpenGL.GLU import *

    load_me = b'img_test.png'
    #~ tex_ID = GLuint(0)
    tex_ID = 0

    def draw_gl_scene():
        theta = time.clock() * 0.1

        ref_mag = 0.1
        tex_u_max = 1.0
        tex_v_max = 1.0

        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glPushMatrix()
        glScalef( 0.8, 0.8, 0.8 )
        glColor4f( 1.0, 1.0, 1.0, 1.0 )
        glNormal3f( 0.0, 0.0, 1.0 )
        glBegin(GL_QUADS)
        glNormal3f( -ref_mag, -ref_mag, 1.0 )
        glTexCoord2f( 0.0, tex_v_max )
        glVertex3f( -1.0, -1.0, -0.1 )

        glNormal3f( ref_mag, -ref_mag, 1.0 )
        glTexCoord2f( tex_u_max, tex_v_max )
        glVertex3f( 1.0, -1.0, -0.1 );

        glNormal3f( ref_mag, ref_mag, 1.0 )
        glTexCoord2f( tex_u_max, 0.0 )
        glVertex3f( 1.0, 1.0, -0.1 )

        glNormal3f( -ref_mag, ref_mag, 1.0 )
        glTexCoord2f( 0.0, 0.0 )
        glVertex3f( -1.0, 1.0, -0.1 )
        glEnd()
        glPopMatrix()
        tex_u_max = 1.0
        tex_v_max = 1.0
        glPushMatrix()
        glScalef( 0.8, 0.8, 0.8 )
        glRotatef(theta, 0.0, 0.0, 1.0)
        glColor4f( 1.0, 1.0, 1.0, 1.0 )
        glNormal3f( 0.0, 0.0, 1.0 )
        glBegin(GL_QUADS)
        glTexCoord2f( 0.0, tex_v_max )
        glVertex3f( 0.0, 0.0, 0.1 )
        glTexCoord2f( tex_u_max, tex_v_max )
        glVertex3f( 1.0, 0.0, 0.1 )
        glTexCoord2f( tex_u_max, 0.0 )
        glVertex3f( 1.0, 1.0, 0.1 )
        glTexCoord2f( 0.0, 0.0 )
        glVertex3f( 0.0, 1.0, 0.1 )
        glEnd()
        glPopMatrix()
        glutSwapBuffers()
        #~ time.sleep(1)

    def keyboard_func(*args):
        if args[0] == '\033':#ESCAPE
            sys.exit()

    def special_func(*args):
        if args[0] == 1:# F1
            try:
                SOIL_save_screenshot(b'screenshot.bmp', ctypes.c_int(SOIL_SAVE_TYPE_BMP), ctypes.c_int(0), ctypes.c_int(0), ctypes.c_int(512), ctypes.c_int(512) )
            except Exception as e:
                print('SOIL_save_screenshot ERROR', e)

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(200, 300)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow(b'SOIL Sample')
    glutSetCursor(GLUT_CURSOR_FULL_CROSSHAIR)
    glutDisplayFunc(draw_gl_scene)
    glutKeyboardFunc(keyboard_func)
    glutSpecialFunc(special_func)

    glEnable( GL_BLEND )
    glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )
    glEnable( GL_ALPHA_TEST )
    glAlphaFunc( GL_GREATER, 0.5 )
    print('Attempting to load as a cubemap')
    time_me = time.clock()
    try:
        tex_ID = SOIL_load_OGL_single_cubemap(load_me, SOIL_DDS_CUBEMAP_FACE_ORDER, SOIL_LOAD_AUTO, SOIL_CREATE_NEW_ID, SOIL_FLAG_POWER_OF_TWO | SOIL_FLAG_MIPMAPS | SOIL_FLAG_DDS_LOAD_DIRECT)
    except Exception as e:
        print('SOIL_load_OGL_single_cubemap ERROR', e)
    time_me = time.clock() - time_me
    print('the load time was ', time_me, ' seconds (warning: low resolution timer)')
    if tex_ID > 0:
        glEnable( GL_TEXTURE_CUBE_MAP )
        glEnable( GL_TEXTURE_GEN_S )
        glEnable( GL_TEXTURE_GEN_T )
        glEnable( GL_TEXTURE_GEN_R )
        glTexGeni( GL_S, GL_TEXTURE_GEN_MODE, GL_REFLECTION_MAP )
        glTexGeni( GL_T, GL_TEXTURE_GEN_MODE, GL_REFLECTION_MAP )
        glTexGeni( GL_R, GL_TEXTURE_GEN_MODE, GL_REFLECTION_MAP )
        glBindTexture( GL_TEXTURE_CUBE_MAP, tex_ID )
        print('the loaded single cube map ID was ', tex_ID)
    else:
        print('Attempting to load as a HDR texture')
        time_me = time.clock()
        try:
            tex_ID = SOIL_load_OGL_HDR_texture(load_me, SOIL_HDR_RGBdivA2, 0, SOIL_CREATE_NEW_ID, SOIL_FLAG_POWER_OF_TWO | SOIL_FLAG_MIPMAPS)
        except Exception as e:
            print('SOIL_load_OGL_HDR_texture ERROR', e)
        time_me = time.clock() - time_me
        print('the load time was ', time_me, ' seconds (warning: low resolution timer)')
        if tex_ID < 1:
            print('Attempting to load as a simple 2D texture')
            time_me = time.clock()
            try:
                tex_ID = SOIL_load_OGL_texture(load_me, SOIL_LOAD_AUTO, SOIL_CREATE_NEW_ID, SOIL_FLAG_POWER_OF_TWO | SOIL_FLAG_MIPMAPS | SOIL_FLAG_DDS_LOAD_DIRECT)
            except Exception as e:
                print('SOIL_load_OGL_texture ERROR', e)
            time_me = time.clock() - time_me
            print('the load time was ', time_me, ' seconds (warning: low resolution timer)')
        if tex_ID > 0:
            glEnable( GL_TEXTURE_2D )
            glBindTexture( GL_TEXTURE_2D, tex_ID )
            print('the loaded texture ID was ', tex_ID)
        else:
            glDisable( GL_TEXTURE_2D )
            print('Texture loading failed: "', SOIL_last_result(), '"')

    glutMainLoop()
