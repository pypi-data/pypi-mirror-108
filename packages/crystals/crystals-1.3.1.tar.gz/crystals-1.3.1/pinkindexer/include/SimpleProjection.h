#pragma once

#include "ReciprocalToRealProjection.h"
#include <Eigen/Dense>

namespace pinkIndexer
{
    class SimpleProjection : public ReciprocalToRealProjection
    {
      public:
        SimpleProjection(const ExperimentSettings& experimentSettings);

        void project(Eigen::Matrix2Xf& projectedPeaks, const Eigen::Matrix3Xf& reciprocalPeaks) const;
    };
} // namespace pinkIndexer