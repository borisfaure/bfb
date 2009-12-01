/*****************************************************************************
 *     C code used to generate a brainfuck program into a C executable       *
 *                                                                           *
 *               Copyright (C) 2009 Boris 'billiob' Faure                    *
 * This code is under the DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE        *
 * Version 2                                                                 *
 *                                                                           *
 *                                                                           *
 * If you want to compile BF++ code, define BFPP                             *
 * If you want your BF++ code to have SSL sockets, define BFPP_SSL           *
 *****************************************************************************/

#ifdef BFPP_SSL
  #ifndef BFPP
    #define BFPP
  #endif
#endif

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef BFPP
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/types.h>
#include <netdb.h>
#include <netinet/in.h>
#include <sys/socket.h>
#endif

#ifdef BFPP_SSL
#include <openssl/bio.h>
#include <openssl/ssl.h>
#include <openssl/err.h>
#endif

#ifdef BFPP
static int sd = -1;
static unsigned char sbuf[4096];
static unsigned char *sbufpos;
static int slen;
#ifdef BFPP_SSL
static BIO *bio = NULL;
static SSL *ssl = NULL;
static SSL_CTX *ctx = NULL;
#endif

static int fd = -1;
static unsigned char fbuf[4096];
static unsigned char *fbufpos;
static int flen;
#endif


void bf_socket_open_close(unsigned char *r, unsigned char **ptr)
{
#ifdef BFPP
    if (sd >= 0) {
#ifdef BFPP_SSL
        if (bio) {
            BIO_free_all(bio);
            bio = NULL;
        } else {
#endif
            close(sd);
            sd = -1;
#ifdef BFPP_SSL
        }
#endif
        return;
    } else {
        unsigned char *colon = strchr(*ptr, ':');
        unsigned char *colonops = strchr(colon + 1, ':');

        if (!colon) {return;}

#ifdef BFPP_SSL
        if (colonops && strncmp(colonops+1, "ssl", 3) == 0 ) {
            *colonops = '\0';
            if (!ctx) {
                ctx = SSL_CTX_new(SSLv23_client_method());
            }

            bio = BIO_new_ssl_connect(ctx);
            BIO_get_ssl(bio, &ssl);
            SSL_set_mode(ssl, SSL_MODE_AUTO_RETRY);
            BIO_set_conn_hostname(bio, *ptr);
            if (BIO_do_connect(bio) <= 0) {
                *colonops = ':';
                BIO_free_all(bio);
                bio = NULL;
                goto error;
            }
            *colonops = ':';
        } else {
#endif
            struct addrinfo hints, *res, *res0;
            int error;
            int s;
            long lport;
            uint16_t port;

            lport = strtol(colon+1, NULL, 10);
            port = htons(lport);
            *colon = '\0';

            memset(&hints, 0, sizeof(hints));
            hints.ai_family = PF_INET;
            hints.ai_socktype = SOCK_STREAM;
            hints.ai_protocol = IPPROTO_TCP;
            error = getaddrinfo(*ptr, NULL, &hints, &res0);
            if (error) {
                *colon = ':';
                goto error;
            }
            for (res = res0; res; res = res->ai_next) {
                sd = socket(res->ai_family, res->ai_socktype, res->ai_protocol);
                if (sd < 0) {
                    continue;
                }

                ((struct sockaddr_in*)res->ai_addr)->sin_port = port;
                if (connect(sd, res->ai_addr, res->ai_addrlen) < 0) {
                    close(sd);
                    sd = -1;
                    continue;
                }

                break;  /* okay we got one */
            }
            freeaddrinfo(res0);
            *colon = ':';
            if (sd < 0) {
                goto error;
            }
#ifdef BFPP_SSL
        }
#endif
    }
    memset(sbuf, 0, sizeof(sbuf));
    sbufpos = NULL;
    slen = 0;
    **ptr = 0;
    return;
  error:
    **ptr = 0xff;
#endif
}

void bf_socket_send(unsigned char *r, unsigned char **ptr)
{
#ifdef BFPP
#ifdef BFPP_SSL
    if (bio) {
        BIO_write(bio, *ptr, 1);
    } else {
#endif
        if (sd >= 0) {
            send(sd, *ptr, 1, 0);
        }
#ifdef BFPP_SSL
    }
#endif
#endif
}

void bf_socket_read(unsigned char *r, unsigned char **ptr)
{
#ifdef BFPP
    if (sbufpos) {
        **ptr = *sbufpos;
        sbufpos++;
        if ((sbufpos - sbuf) >= slen) {
            memset(sbuf, 0, sizeof(sbuf));
            sbufpos = NULL;
            slen = 0;
        }
    } else {
#ifdef BFPP_SSL
        if (bio) {
            slen = BIO_read(bio, sbuf, sizeof(sbuf));
            if (slen <= 0) {
                **ptr = 0;
            } else {
                sbufpos = sbuf;
                **ptr = *sbufpos;
                sbufpos++;
            }
        } else {
#endif
            if (sd >= 0) {
                slen = recv(sd, sbuf, sizeof(sbuf), 0);
                if (slen <= 0) {
                    **ptr = 0;
                } else {
                    sbufpos = sbuf;
                    **ptr = *sbufpos;
                    sbufpos++;
                }
            } else {
                **ptr = 0;
            }
#ifdef BFPP_SSL
        }
#endif
    }
#endif
}

void bf_file_open_close(unsigned char *r, unsigned char **ptr)
{
#ifdef BFPP
    if (fd < 0) {
        fd = open(*ptr, O_RDWR|O_CREAT, 0777);
        if (fd) {
            memset(fbuf, 0, sizeof(fbuf));
            fbufpos = NULL;
            flen = 0;
            **ptr = 0;
        } else {
            **ptr = 0xff;
        }
    } else {
        close(fd);
        fd = -1;
    }
#endif
}

void bf_file_write(unsigned char *r, unsigned char **ptr)
{
#ifdef BFPP
    if (fd >= 0)
        write(fd, *ptr, 1);
#endif
}

void bf_file_read(unsigned char *r, unsigned char **ptr)
{
#ifdef BFPP
    if (fbufpos) {
        **ptr = *fbufpos;
        fbufpos++;
        if ((fbufpos - fbuf) >= flen) {
            memset(fbuf, 0, sizeof(fbuf));
            fbufpos = NULL;
            flen = 0;
        }
    } else {
        if (fd >= 0) {
            flen = read(fd, fbuf, sizeof(fbuf), 0);
            if (flen <= 0) {
                **ptr = 0;
            } else {
                fbufpos = fbuf;
                **ptr = *fbufpos;
                fbufpos++;
            }
        } else {
            **ptr = 0;
        }
    }
#endif
}


void bf_debug(unsigned char *r, unsigned char **ptr)
{
    /* TODO */
}


int main() {
    unsigned char *r = calloc(30000, sizeof(unsigned char));
    unsigned char *ptr = r;

#ifdef BFPP_SSL
    SSL_library_init();
    ERR_load_crypto_strings();
    ERR_load_SSL_strings();
#endif


/* HERE GOES THE BRAINFUCK CODE :) */
