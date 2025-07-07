#include "com_arqma_arqnet_ArqnetVPN.h"
#include "arqnet_jni_vpnio.hpp"
#include "arqnet_jni_common.hpp"
#include <net/ip.hpp>

extern "C"
{
  JNIEXPORT jint JNICALL
  Java_com_arqma_arqnet_ArqnetVPN_PacketSize(JNIEnv *, jclass)
  {
    return llarp::net::IPPacket::MaxSize;
  }

  JNIEXPORT jobject JNICALL
  Java_com_arqma_arqnet_ArqnetVPN_Alloc(JNIEnv *env, jclass)
  {
    arqnet_jni_vpnio *vpn = new arqnet_jni_vpnio();
    return env->NewDirectByteBuffer(vpn, sizeof(arqnet_jni_vpnio));
  }

  JNIEXPORT void JNICALL
  Java_com_arqma_arqnet_ArqnetVPN_Free(JNIEnv *env, jclass, jobject buf)
  {
    arqnet_jni_vpnio *vpn = FromBuffer< arqnet_jni_vpnio >(env, buf);
    if(vpn == nullptr)
      return;
    delete vpn;
  }
  JNIEXPORT void JNICALL
  Java_com_arqma_arqnet_ArqnetVPN_Stop(JNIEnv *env, jobject self)
  {
    arqnet_jni_vpnio *vpn = GetImpl< arqnet_jni_vpnio >(env, self);
    if(vpn)
    {
      vpn->Close();
    }
  }

  JNIEXPORT jint JNICALL
  Java_com_arqma_arqnet_ArqnetVPN_ReadPkt(JNIEnv *env, jobject self,
                                               jobject pkt)
  {
    arqnet_jni_vpnio *vpn = GetImpl< arqnet_jni_vpnio >(env, self);
    if(vpn == nullptr)
      return -1;
    void *pktbuf = env->GetDirectBufferAddress(pkt);
    auto pktlen  = env->GetDirectBufferCapacity(pkt);
    if(pktbuf == nullptr)
      return -1;
    return vpn->ReadPacket(pktbuf, pktlen);
  }

  JNIEXPORT jboolean JNICALL
  Java_com_arqma_arqnet_ArqnetVPN_WritePkt(JNIEnv *env, jobject self,
                                                jobject pkt)
  {
    arqnet_jni_vpnio *vpn = GetImpl< arqnet_jni_vpnio >(env, self);
    if(vpn == nullptr)
      return false;
    void *pktbuf = env->GetDirectBufferAddress(pkt);
    auto pktlen  = env->GetDirectBufferCapacity(pkt);
    if(pktbuf == nullptr)
      return false;
    return vpn->WritePacket(pktbuf, pktlen);
  }

  JNIEXPORT void JNICALL
  Java_com_arqma_arqnet_ArqnetVPN_SetInfo(JNIEnv *env, jobject self,
                                               jobject info)
  {
    arqnet_jni_vpnio *vpn = GetImpl< arqnet_jni_vpnio >(env, self);
    if(vpn == nullptr)
      return;
    VisitObjectMemberStringAsStringView< bool >(
        env, info, "ifaddr", [vpn](llarp::string_view val) -> bool {
          vpn->SetIfAddr(val);
          return true;
        });
    VisitObjectMemberStringAsStringView< bool >(
        env, info, "ifname", [vpn](llarp::string_view val) -> bool {
          vpn->SetIfName(val);
          return true;
        });
    vpn->info.netmask = GetObjectMemberAsInt< uint8_t >(env, info, "netmask");
  }
}