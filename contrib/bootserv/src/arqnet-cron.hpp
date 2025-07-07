#ifndef BOOTSERV_ARQNET_CRON_HPP
#define BOOTSERV_ARQNET_CRON_HPP

#include "handler.hpp"

namespace arqnet
{
  namespace bootserv
  {
    struct CronHandler final : public Handler
    {
      CronHandler(std::ostream& o);
      ~CronHandler();

      int
      Exec(const Config& conf) override;

      int
      ReportError(const char* err) override;
    };

  }  // namespace bootserv
}  // namespace arqnet

#endif
