#pragma once

#include <chrono>
#include <cstdint>
#include <string>

namespace pinkIndexer
{
    class Chronometer
    {
      public:
        /**
         * @brief Chronometer constructor - saves the current time
         * @param key the key for the debug protocol value
         */
        Chronometer(const std::string& key);
        /**
         * @brief Chronometer destructor - gets the current time, calculates the
         * difference to the saved time (in milliseconds) and logs it via the Debug class
         */
        ~Chronometer();

      private:
        /// the key for the time value
        const std::string key_;
        /// the timestamp at object construction
        std::chrono::time_point<std::chrono::system_clock> startTime_;
    };
} // namespace pinkIndexer