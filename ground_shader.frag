#version 150

// Vertex position (in camera space)
in vec3 vPositionCam;

// Surface Normal (in camera space)
in vec3 normalCam;

// Light position (in camera space)
in vec3 lightPositionCam;

// Texture Coordinates
in vec2 texCoords;

// Light intensities for ambient, diffuse and specular components
uniform vec3 I_a;
uniform vec3 I_d;
uniform vec3 I_s;

// Material properties for ambient, diffuse and specular lighting
uniform vec3 k_a;
uniform vec3 k_d;
uniform vec3 k_s;

// Shininess (specular exponent)
uniform float n;

// Texture to be mapped to object
uniform sampler2D tex;

// Fragment color
out vec4 finalColor;

void main()
{
    // Calculate the required N, L, R and V vectors
    vec3 N = normalize(normalCam);
    vec3 L = normalize(lightPositionCam - vPositionCam);
    vec3 R = normalize(reflect(-L, N));
    vec3 V = normalize(-vPositionCam);

    // Calculate ambient, diffuse and specular components
    vec3 ambient = I_a * k_a;
    vec3 diffuse = I_d * k_d * max(dot(L, N), 0.0);
    vec3 specular = I_s * k_s * pow(max(dot(R, V), 0.0), n);

    // Get the texture value for the current fragment
    vec4 texColor = texture(tex, texCoords);

    // Set the final fragment color
    finalColor = vec4(ambient + diffuse, 1.0) * texColor + vec4(specular, 1.0);
}
