#ifndef LLARP_UTIL_ARQNET_INIT_H
#define LLARP_UTIL_ARQNET_INIT_H

#ifdef __cplusplus
extern "C"
{
#endif

#ifndef Arqnet_INIT
#if defined(_WIN32)
#define Arqnet_INIT \
  DieInCaseSomehowThisGetsRunInWineButLikeWTFThatShouldNotHappenButJustInCaseHandleItWithAPopupOrSomeShit
#else
#define Arqnet_INIT _arqnet_non_shit_platform_INIT
#endif
#endif

  int
  Arqnet_INIT(void);

#ifdef __cplusplus
}
#endif
#endif