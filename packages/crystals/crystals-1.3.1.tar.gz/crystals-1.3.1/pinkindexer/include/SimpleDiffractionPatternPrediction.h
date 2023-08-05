#pragma once


#include "SimpleProjection.h"
#include <Eigen/Dense>

namespace pinkIndexer
{
    class SimpleDiffractionPatternPrediction
    {
      public:
        SimpleDiffractionPatternPrediction(const ExperimentSettings& experimentSettings);

        void getPeaksOnEwaldSphere(Eigen::Matrix3Xf& peaksOnEwaldSphere, Eigen::Matrix3Xi& millerIndices, const Lattice& lattice);
        void predictPattern(Eigen::Matrix2Xf& predictedPeaks, Eigen::Matrix3Xi& millerIndices, Eigen::Matrix3Xf& projectionDirections, const Lattice& lattice);

      private:
        SimpleProjection reciprocalToRealProjection;

        float maxResolutionAngle;
        float reflectionRadius;
        float reciprocalLambdaShort, reciprocalLambdaLong;
        float reciprocalLambdaShort_extended_squared, reciprocalLambdaLong_extended_squared;
        float detectorDistance;
    };
} // namespace pinkIndexer