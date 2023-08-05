#pragma once

#include "ExperimentSettings.h"
#include <Eigen/Dense>

namespace pinkIndexer
{
    class ReciprocalToRealProjection
    {
      public:
        ReciprocalToRealProjection(const ExperimentSettings& experimentSettings);
        virtual ~ReciprocalToRealProjection() = default;

        virtual void project(Eigen::Matrix2Xf& projectedPoints, const Eigen::Matrix3Xf& reciprocalPoints) const = 0;

      protected:
        ExperimentSettings experimentSettings;
    };
} // namespace pinkIndexer