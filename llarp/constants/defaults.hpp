#ifndef LLARP_DEFAULTS_HPP
#define LLARP_DEFAULTS_HPP

#ifndef DEFAULT_RESOLVER_US
#define DEFAULT_RESOLVER_US "1.1.1.1"
#endif
#ifndef DEFAULT_RESOLVER_EU
#define DEFAULT_RESOLVER_EU "1.1.1.1"
#endif
#ifndef DEFAULT_RESOLVER_AU
#define DEFAULT_RESOLVER_AU "1.1.1.1"
#endif

#ifdef DEBIAN
#ifndef DEFAULT_ARQNET_USER
#define DEFAULT_ARQNET_USER "debian-arqnet"
#endif
#ifndef DEFAULT_ARQNET_GROUP
#define DEFAULT_ARQNET_GROUP "debian-arqnet"
#endif
#else
#ifndef DEFAULT_ARQNET_USER
#define DEFAULT_ARQNET_USER "arqnet"
#endif
#ifndef DEFAULT_ARQNET_GROUP
#define DEFAULT_ARQNET_GROUP "arqnet"
#endif
#endif

#endif
