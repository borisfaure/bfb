/*****************************************************************************
 *     C code used to generate a brainfuck program into a C executable       *
 *                                                                           *
 *            Copyright (C) 2009-2011 Boris 'billiob' Faure                  *
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
#include <unistd.h>
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

#define BUFSZ 4096

#ifdef BFPP
static int sd = -1;
static char sbuf[BUFSZ];
static char *sbufpos;
static int slen;
#ifdef BFPP_SSL
static BIO *bio = NULL;
static SSL *ssl = NULL;
static SSL_CTX *ctx = NULL;
#endif

static int fd = -1;
static char fbuf[BUFSZ];
static char *fbufpos;
static int flen;
#endif


void bf_socket_open_close(char **ptr)
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
        char *colon = strchr(*ptr, ':');
        char *colonops = strchr(colon + 1, ':');

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

void bf_socket_send(char **ptr)
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

void bf_socket_read(char **ptr)
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

void bf_file_open_close(char **ptr)
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

void bf_file_write(char **ptr)
{
#ifdef BFPP
    if (fd >= 0)
        write(fd, *ptr, 1);
#endif
}

void bf_file_read(char **ptr)
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
            flen = read(fd, fbuf, sizeof(fbuf));
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

void print_pos(char *r, unsigned int i)
{
    char v;
    if (i < 30000) {
        v = *(r+i);
        if ( v >= 33 && v <= 126)
            printf("%d> %d %c |", i, v, v);
        else
            printf("%d> %d |", i, v);
    }
}

#define BF_DEBUG(...)                                                       \
    printf("Current position in the code: line %d of file %s\n",            \
           __LINE__, __FILE__);                                             \
    printf("Print cell range (A-B) (Current pos is %d):\n",                 \
           (int) ( ptr - r ));                                              \
                                                                            \
    if (fgets(debugbuf, BUFSZ, stdin)) {                                    \
        x = strtol(debugbuf, &endptr, 10);                                  \
        if (*endptr == '-') {                                               \
           y = strtol(endptr + 1, NULL, 10);                                \
        }                                                                   \
        if ( x >= 0 && y >= 0 ) {                                           \
            print_pos(r, x);                                                \
            for (i = x+1; i <= y; i++) {                                    \
                print_pos(r, i);                                            \
            }                                                               \
        }                                                                   \
        putchar('\n');                                                      \
    }


int main()
{
    char *r = calloc(30000, sizeof(char));
    char *ptr = r;
    long x = 0, y = 0;
    long i;
    char *endptr;
    char debugbuf[BUFSZ];


#ifdef BFPP_SSL
    SSL_library_init();
    ERR_load_crypto_strings();
    ERR_load_SSL_strings();
#endif


/* HERE GOES THE BRAINFUCK CODE :) */
