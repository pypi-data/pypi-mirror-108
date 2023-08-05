/*
 * BadInput.hpp
 *
 *  Created on: 03.09.2016
 *      Author: Ruhullah
 */

#ifndef BADINPUTEXCEPTION_H_
#define BADINPUTEXCEPTION_H_

#include <CustomException.h>

namespace pinkIndexer
{

    class BadInputException : public CustomException
    {
      public:
        BadInputException(const std::string& msg)
            : CustomException(msg)
        {
        }

        virtual ~BadInputException() throw() {}
    };
} // namespace pinkIndexer

#endif /* BADINPUTEXCEPTION_H_ */
