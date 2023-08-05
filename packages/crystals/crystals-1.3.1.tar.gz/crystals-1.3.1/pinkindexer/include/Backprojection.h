#pragma once

#include "ExperimentSettings.h"
#include <Eigen/Dense>

namespace pinkIndexer
{

    class Backprojection
    {
      public:
        Backprojection(const ExperimentSettings& experimentSettings);

        void backProject(const Eigen::Matrix2Xf& detectorPeaks_m, Eigen::Matrix3Xf& ulsDirections, Eigen::Array2Xf& ulsBorderNorms) const;

      private:
        ExperimentSettings experimentSettings;
    };

} // namespace pinkIndexer