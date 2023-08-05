/*
 * WrongUsageException.h
 *
 *  Created on: 16.04.2017
 *      Author: Yaro
 */

#ifndef WRONGUSAGEEXCEPTION_H_
#define WRONGUSAGEEXCEPTION_H_

#include <CustomException.h>

namespace pinkIndexer
{

    class WrongUsageException : public CustomException
    {
      public:
        WrongUsageException(const std::string& msg)
            : CustomException(msg)
        {
        }

        virtual ~WrongUsageException() throw() {}
    };
} // namespace pinkIndexer
#endif /* WRONGUSAGEEXCEPTION_H_ */
