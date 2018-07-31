IDIR =.

CFLAGS+=-I$(IDIR)

LIBS=$(LDFLAGS)

ODIR =.

prefix=/opt/freeware

bindir=$(prefix)/bin

mandir=$(prefix)/man/man1

HELP2MAN=$(bindir)/help2man

RM=/usr/bin/rm -f

MAN_INSTALL_PATH=$(DESTDIR)$(mandir)

_DEPS = getopt_long.h
DEPS = $(patsubst %,$(IDIR)/%,$(_DEPS))

_OBJ = gzip.o getopt_long.o
OBJ = $(patsubst %,$(ODIR)/%,$(_OBJ))


$(ODIR)/%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

Xgzip: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS) $(LIBS)
	cp Xgzip Xgunzip

Xgzip.1: Xgzip
	LIBPATH=/usr/lib $(HELP2MAN) -N --output=$@ \
		--help-option='-h' --version-option='-V' \
		--name "Gzip using accelerated zlib." ./$<

manpages: Xgzip.1

all: Xgzip manpages

install_Xgzip: Xgzip
	install -D -m 755 Xgzip    -T $(DESTDIR)$(bindir)/Xgzip
	install -D -m 755 Xgunzip -T $(DESTDIR)$(bindir)/Xgunzip

uninstall_Xgzip:
		$(RM) $(DESTDIR)$(bindir)/Xgzip
		$(RM) $(DESTDIR)$(bindir)/Xgunzip

install_manpages: manpages
	@mkdir -p $(MAN_INSTALL_PATH)
	cp -uv Xgzip.1 $(MAN_INSTALL_PATH)

uninstall_manpages:
		echo "removing $(DESTDIR)$(mandir)/Xgzip.1...";   \
		$(RM) $(DESTDIR)$(mandir)/Xgzip.1

install: install_Xgzip install_manpages

uninstall: uninstall_Xgzip uninstall_manpages

.PHONY: clean

clean:
	$(RM) $(ODIR)/*.o *~ Xgzip Xgunzip Xgzip.1
