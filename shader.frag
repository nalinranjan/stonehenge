#version 150

// Vertex position (in camera space)
in vec3 vPositionCam;

// Surface Normal (in camera space)
in vec3 normalCam;

// Light position (in camera space)
in vec3 lightPositionCam;

// Texture Coordinates
in vec2 texCoords;

// Light color
uniform vec3 I_a;
uniform vec3 I_d;
uniform vec3 I_s;

// Reflection coefficients
uniform vec3 k_a;
uniform vec3 k_d;
uniform vec3 k_s;

// Shininess (specular exponent)
uniform float n;
uniform float zero;

// Texture to be mapped to object
uniform sampler2D tex;

// Fragment color
out vec4 finalColor;

in vec3 test;

void main()
{
    // Calculate the required N, L, R and V vectors
    vec3 N = normalize(normalCam);
    vec3 L = normalize(lightPositionCam - vPositionCam);
    vec3 R = normalize(reflect(-L, N));
    vec3 V = normalize(-vPositionCam);

    // Calculate ambient, diffuse and specular components
    vec3 ambient = I_a * k_a;// * zero;
    vec3 diffuse = I_d * k_d * max(dot(L, N), 0.0);// * zero;
    vec3 specular = I_s * k_s * pow(max(dot(R, V), 0.0), n);// * zero;

    vec4 texColor = texture(tex, texCoords);

    // finalColor = texColor * zero;
    finalColor = vec4(ambient + diffuse, 1.0) * texColor + vec4(specular, 1.0);
    // finalColor += vec4(ambient + diffuse + specular, 1.0); // - vec4(texColor);
    // finalColor += vec4(test, 1.0);
}
