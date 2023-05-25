#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h> 
#include <stdio.h>
#include <stddef.h>
#include "openssl/bn.h"
#include "openssl/rsa.h"
#include "openssl/bio.h"
#include "openssl/evp.h"
#include "openssl/pem.h"
#include "openssl/x509.h"

#define BUFFER 1024

RSA *obtener_rsa(char *fichero) {
    X509 *cert;
    EVP_PKEY *pkey;
    RSA *rsa;
    BIO *bio;
    int correcto;

    bio = BIO_new(BIO_s_file());
    correcto = BIO_read_filename(bio, fichero);
    if (correcto != 1) {
        fprintf(stderr, "Error al leer el fichero '%s'.\n", fichero);
        exit(1);
    }

    cert = PEM_read_bio_X509(bio, NULL, 0, NULL);
    if (cert == NULL) {
        fprintf(stderr, "Error al leer el certificado del fichero '%s'.\n", fichero);
        exit(1);
    }

    pkey = X509_get_pubkey(cert);
    rsa = EVP_PKEY_get1_RSA(pkey);

    X509_free(cert);
    EVP_PKEY_free(pkey);
    BIO_free(bio);

    if (rsa == NULL) {
        fprintf(stderr, "Error al obtener la clave RSA del fichero '%s'.\n", fichero);
        exit(1);
    }

    return rsa;
}

int main(int argc, char *argv[]) {
    unsigned char *res;
    unsigned char *sol;
    BN_CTX *ctx;
    RSA *privada;
    BIO *bioprint;
    BIGNUM *one;
    RSA *rsa1;
    BIGNUM *n1;
    BIGNUM *q1;
    RSA *rsa2;
    BIGNUM *n2;
    BIGNUM *q2;
    BIGNUM *p;
    BIGNUM *total;
    BIGNUM *fi1;
    BIGNUM *fi2;
    BIGNUM *e;
    BIGNUM *d;
    int fd;
    int len;

    if (argc != 4) {
        fprintf(stderr, "Uso: %s <fichero1> <fichero2> <fichero3>\n", argv[0]);
        exit(1);
    }

    res = malloc(sizeof(unsigned char) * BUFFER);
    if (res == NULL) {
        fprintf(stderr, "Error al reservar memoria para res.\n");
        exit(1);
    }

    sol = malloc(sizeof(unsigned char) * BUFFER);
    if (sol == NULL) {
        fprintf(stderr, "Error al reservar memoria para sol.\n");
        exit(1);
    }

    ctx = BN_CTX_new();
    if (ctx == NULL) {
        fprintf(stderr, "Error al crear el contexto BN_CTX.\n");
        exit(1);
    }

    bioprint = BIO_new_fp(stdout, BIO_NOCLOSE);
    if (bioprint == NULL) {
        fprintf(stderr, "Error al crear el objeto BIO para imprimir.\n");
        exit(1);
    }

    rsa1 = obtener_rsa(argv[1]);
    rsa2 = obtener_rsa(argv[2]);

    one = BN_new();
    q1 = BN_new();
    q2 = BN_new();
    p = BN_new();
    d = BN_new();
    total = BN_new();
    fi1 = BN_new();
    fi2 = BN_new();
    privada = RSA_new();

    n1 = RSA_get0_n(rsa1);
    if (n1 == NULL) {
        fprintf(stderr, "Error al obtener el valor de n1.\n");
        exit(1);
    }

    n2 = RSA_get0_n(rsa2);
    if (n2 == NULL) {
        fprintf(stderr, "Error al obtener el valor de n2.\n");
        exit(1);
    }

    e = RSA_get0_e(rsa1);
    if (e == NULL) {
        fprintf(stderr, "Error al obtener el valor de e.\n");
        exit(1);
    }

    BN_gcd(p, n1, n2, ctx);
    BN_div(q1, NULL, n1, p, ctx);
    BN_div(q2, NULL, n2, p, ctx);

    BN_dec2bn(&one, "1");
    BN_sub(fi1, q1, one);
    BN_sub(fi2, p, one);
    BN_mul(total, fi1, fi2, ctx);
    BN_mod_inverse(d, e, total, ctx);

    RSA_set0_key(privada, n1, e, d);
    RSA_set0_factors(rsa1, p, q1);
    RSA_set0_factors(rsa2, p, q2);

    printf("\nCERTIFICADO 1:\n");
    RSA_print(bioprint, rsa1, 0);
    RSA_print(bioprint, privada, 0);

    printf("\nCERTIFICADO 2:\n");
    RSA_print(bioprint, rsa2, 0);
    RSA_print(bioprint, privada, 0);

    fd = open(argv[3], O_RDONLY);
    if (fd == -1) {
        fprintf(stderr, "Error al abrir el fichero '%s'.\n", argv[3]);
        exit(1);
    }

    len = read(fd, res, BUFFER);
    if (len == -1) {
        fprintf(stderr, "Error al leer el fichero '%s'.\n", argv[3]);
        exit(1);
    }

    RSA_private_decrypt(len, res, sol, privada, RSA_PKCS1_PADDING);

    printf("\nTexto encriptado:\n");
    fwrite(res, sizeof(unsigned char), len, stdout);

    printf("\nTexto desencriptado:\n");
    fwrite(sol, sizeof(unsigned char), len, stdout);

    free(res);
    free(sol);

    BN_CTX_free(ctx);
    BIO_free(bioprint);

    BN_free(one);
    BN_free(n1);
    BN_free(q1);
    BN_free(n2);
    BN_free(q2);

    BN_free(p);
    BN_free(d);
    BN_free(e);

    BN_free(total);
    BN_free(fi1); 
    BN_free(fi2);
    
    RSA_free(privada);
    RSA_free(rsa1);
    RSA_free(rsa2);

    return 0;
}





