#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/types.h>
#include <netdb.h>
#include <netinet/in.h>
#include <sys/socket.h>

static int sd = -1;
static unsigned char sbuf[4096];
static unsigned char *sbufpos;
static int slen;

static int fd = -1;
static unsigned char fbuf[4096];
static unsigned char *fbufpos;
static int flen;


void bf_socket_open_close(unsigned char *r, unsigned char **ptr)
{
    if (sd >= 0) {
        close(sd);
        sd = -1;
    } else {
        struct addrinfo hints, *res, *res0;
        int error;
        int s;
        unsigned char *colon = strchr(*ptr, ':');
        long lport;
        uint16_t port;

        if (!colon) {return;}

        lport = strtol(colon+1, NULL, 10);
        port = htons(lport);
        *colon = '\0';

        memset(&hints, 0, sizeof(hints));
        hints.ai_family = PF_INET;
        hints.ai_socktype = SOCK_STREAM;
        hints.ai_protocol = IPPROTO_TCP;
        error = getaddrinfo(*ptr, NULL, &hints, &res0);
        if (error) {
            **ptr = 0xff;
            return;
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
            **ptr = 0xff;
        } else {
            memset(sbuf, 0, sizeof(sbuf));
            sbufpos = NULL;
            slen = 0;
            **ptr = 0;
        }
    }
}

void bf_socket_send(unsigned char *r, unsigned char **ptr)
{
    if (sd >= 0) {
        send(sd, *ptr, 1, 0);
    }
}

void bf_socket_read(unsigned char *r, unsigned char **ptr)
{
    if (sbufpos) {
        **ptr = *sbufpos;
        sbufpos++;
        if ((sbufpos - sbuf) >= slen) {
            memset(sbuf, 0, sizeof(sbuf));
            sbufpos = NULL;
            slen = 0;
        }
    } else {
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
    }
}

void bf_file_open_close(unsigned char *r, unsigned char **ptr)
{
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
    }
}

void bf_file_write(unsigned char *r, unsigned char **ptr)
{
    if (fd >= 0)
        write(fd, *ptr, 1);
}

void bf_file_read(unsigned char *r, unsigned char **ptr)
{
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
}


void bf_debug(unsigned char *r, unsigned char **ptr)
{
    /* TODO */
}


int main() {
    unsigned char *r = calloc(30000, sizeof(unsigned char));
    unsigned char *ptr = r;



