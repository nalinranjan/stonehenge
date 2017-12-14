#version 150

// Vertex location (in model space)
in vec3 vPosition;

// Normal vector at vertex (in model space)
in vec3 vNormal;

// Transformation matrices
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

// Light position (in world space)
uniform vec3 lightPosition;

// Vertex position (in camera space)
out vec3 vPositionCam;

// Surface Normal (in camera space)
out vec3 normalCam;

// Light position (in camera space)
out vec3 lightPositionCam;

void main()
{
    // Generate the model-view and normal matrices
    mat4 modelView = view * model;
    mat3 normalMatrix = mat3(transpose(inverse(modelView)));

    // Transform vertex, light and normal to camera space
    vPositionCam = vec3(modelView * vec4(vPosition, 1.0));
    normalCam = normalize(normalMatrix * vNormal);
    lightPositionCam = mat3(view) * lightPosition;

    // Transform the vertex location into clip space
    gl_Position =  projection * view * model * vec4(vPosition, 1.0);
}
