#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdio.h>

// Librerías necesarias para este proyecto (OpenSSL)
#include "openssl/bn.h"
#include "openssl/rsa.h"
#include "openssl/bio.h"
#include "openssl/evp.h"
#include "openssl/pem.h"
#include "openssl/x509.h"

#define BUFFER 1024

/**
 * Cargar un certificado RSA desde un archivo.
 *
 * @param ruta   Ruta del archivo.
 *
 * @return  Clave RSA cargada.
 */
RSA *cargar_rsa_desde_archivo(char *ruta) {
    X509 *certificado;
    EVP_PKEY *clave_publica;
    RSA *rsa;
    BIO *buffer_entrada;
    int lectura_correcta;

    buffer_entrada = BIO_new(BIO_s_file());
    lectura_correcta = BIO_read_filename(buffer_entrada, ruta);

    if (lectura_correcta != 1) {
        printf("Error al leer el archivo '%s'.\n", ruta);
        exit(1);
    }

    certificado = PEM_read_bio_X509(buffer_entrada, NULL, 0, NULL);
    if (certificado == NULL) {
        printf("Error al leer el certificado del archivo '%s'.\n", ruta);
        exit(1);
    }

    clave_publica = X509_get_pubkey(certificado);
    if (clave_publica == NULL) {
        printf("Error al obtener la clave pública del certificado del archivo '%s'.\n", ruta);
        exit(1);
    }

    rsa = EVP_PKEY_get1_RSA(clave_publica);
    if (rsa == NULL) {
        printf("Error al obtener la clave RSA del certificado del archivo '%s'.\n", ruta);
        exit(1);
    }

    X509_free(certificado);
    EVP_PKEY_free(clave_publica);
    BIO_free(buffer_entrada);

    return rsa;
}

/**
 * Método principal.
 *
 * @return  0 si correcto.
 */
int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Debe proporcionar dos rutas a archivos que contengan certificados RSA.\n");
        return 1;
    }

    RSA *rsa1 = cargar_rsa_desde_archivo(argv[1]);
    RSA *rsa2 = cargar_rsa_desde_archivo(argv[2]);

    if (rsa1 == NULL || rsa2 == NULL) {
        printf("Uno o ambos archivos proporcionados no contienen un certificado RSA válido.\n");
        return 1;
    }

    unsigned char *resultado = malloc(sizeof(unsigned char) * BUFFER);
    unsigned char *solucion = malloc(sizeof(unsigned char) * BUFFER);

    BN_CTX *contexto = BN_CTX_new();

    BIO *bio_salida = BIO_new_fp(stdout, BIO_NOCLOSE);

    BIGNUM *n1 = BN_new();
    BIGNUM *n2 = BN_new();
    BIGNUM *q1 = BN_new();
    BIGNUM *q2 = BN_new();
    BIGNUM *p_comun = BN_new();
    BIGNUM *total = BN_new();
    BIGNUM *fi1 = BN_new();
    BIGNUM *fi2 = BN_new();
    BIGNUM *exponente_publico = BN_new();
    BIGNUM *exponente_privado = BN_new();
    BIGNUM *uno = BN_new();
    RSA *clave_privada = RSA_new();

    if (n1 == NULL || n2 == NULL || q1 == NULL || q2 == NULL || p_comun == NULL
        || total == NULL || fi1 == NULL || fi2 == NULL || exponente_publico == NULL
        || exponente_privado == NULL || uno == NULL || clave_privada == NULL) {
        printf("Error al reservar memoria para las variables.\n");
        return 1;
    }

    if (BN_dec2bn(&uno, "1") == 0) {
        printf("Error al inicializar la variable 'uno'.\n");
        return 1;
    }

    if (RSA_get0_n(rsa1, &n1) == 0 || RSA_get0_n(rsa2, &n2) == 0 || RSA_get0_e(rsa1, &exponente_publico) == 0) {
        printf("Error al obtener los valores de las claves RSA.\n");
        return 1;
    }

    if (BN_gcd(p_comun, n1, n2, contexto) == 0 || BN_div(q1, NULL, n1, p_comun, contexto) == 0
        || BN_div(q2, NULL, n2, p_comun, contexto) == 0) {
        printf("Error al calcular los valores de p y q.\n");
        return 1;
    }

    if (BN_sub(fi1, q1, uno) == 0 || BN_sub(fi2, p_comun, uno) == 0 || BN_mul(total, fi1, fi2, contexto) == 0
        || BN_mod_inverse(exponente_privado, exponente_publico, total, contexto) == 0
        || RSA_set0_key(clave_privada, n1, exponente_publico, exponente_privado) == 0
        || RSA_set0_factors(rsa1, p_comun, q1) == 0 || RSA_set0_factors(rsa2, p_comun, q2) == 0) {
        printf("Error al calcular los valores de la clave privada.\n");
        return 1;
    }

    printf("\nCERTIFICADO 1:\n");
    RSA_print(bio_salida, rsa1, 0);
    RSA_print(bio_salida, clave_privada, 0);

    printf("\nCERTIFICADO 2:\n");
    RSA_print(bio_salida, rsa2, 0);
    RSA_print(bio_salida, clave_privada, 0);

    int descriptor_archivo = open("mensaje.txt", O_RDONLY);
    if (descriptor_archivo == -1) {
        printf("Error al abrir el archivo 'mensaje.txt'.\n");
        return 1;
    }

    int longitud = read(descriptor_archivo, resultado, BUFFER);
    close(descriptor_archivo);

    if (longitud == -1) {
        printf("Error al leer el archivo 'mensaje.txt'.\n");
        return 1;
    }

    if (RSA_private_decrypt(longitud, resultado, solucion, clave_privada, RSA_PKCS1_PADDING) == -1) {
        printf("Error al descifrar el mensaje.\n");
        return 1;
    }

    printf("\nMensaje descifrado: %s\n", solucion);

    // Liberar memoria
    free(resultado);
    free(solucion);
    BN_CTX_free(contexto);
    RSA_free(rsa1);
    RSA_free(rsa2);
    RSA_free(clave_privada);
    BIO_free_all(bio_salida);
    BN_free(uno);
    BN_free(p_comun);
    BN_free(q1);
    BN_free(q2);
    BN_free(total);
    BN_free(fi1);
    BN_free(fi2);
    BN_free(exponente_privado);

    return 0;
}