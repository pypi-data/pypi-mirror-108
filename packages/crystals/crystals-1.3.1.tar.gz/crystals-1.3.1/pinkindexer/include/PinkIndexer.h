#pragma once


#include "Backprojection.h"
#include "ExperimentSettings.h"
#include "Lattice.h"
#include "Refinement.h"
#include "SimpleDiffractionPatternPrediction.h"
#include "SimpleProjection.h"
#include "Sinogram.h"
#include <Eigen/Dense>
#include <stdint.h>

namespace pinkIndexer
{

    class PinkIndexer
    {
      public:
        enum class ConsideredPeaksCount
        {
            veryFew,
            few,
            standard,
            many,
            manyMany
        };

        enum class AngleResolution
        {
            extremelyLoose,
            loose,
            standard,
            dense,
            extremelyDense
        };

        enum class RefinementType
        {
            none,
            fixedLatticeParameters,
            variableLatticeParameters,
            firstFixedThenVariableLatticeParameters,
            firstFixedThenVariableLatticeParametersMultiSeedLengths,
            firstFixedThenVariableLatticeParametersMultiSeed,
            firstFixedThenVariableLatticeParametersCenterAdjustmentMultiSeed
        };

        PinkIndexer(const ExperimentSettings& experimentSettings, ConsideredPeaksCount consideredPeaksCount, AngleResolution angleResolution,
                    RefinementType refinementType, float maxResolutionForIndexing_1_per_A);

		// main function
        int indexPattern(Lattice& indexedLattice, Eigen::Vector2f& centerShift, Eigen::Array<bool, Eigen::Dynamic, 1>& fittedPeaks,
                         Eigen::RowVectorXf& intensities, const Eigen::Matrix2Xf& detectorPeaks_m, int threadCount);
        // for crystfel
		int indexPattern(Lattice& indexedLattice, Eigen::Vector2f& centerShift, Eigen::Array<bool, Eigen::Dynamic, 1>& fittedPeaks,
                         Eigen::RowVectorXf& intensities, const Eigen::Matrix3Xf& meanReciprocalPeaks_1_per_A, int threadCount);

      private:
		// reduces number of peaks according to parameter "ConsideredPeaksCount"
        void reducePeakCount(Eigen::Matrix3Xf& ulsDirections, Eigen::Array2Xf& ulsBorderNorms, Eigen::RowVectorXf& intensities,
                             const Eigen::Matrix2Xf& detectorPeaks_m);
        void refine(Lattice& indexedLattice, Eigen::Vector2f& centerShift, const Eigen::Matrix3Xf& ulsDirections, const Eigen::Array2Xf& ulsBorderNorms,
                    const Eigen::Matrix2Xf& detectorPeaks_m, int threadCount);

        float getAngleResolution();
        int getConsideredPeaksCount();

        SimpleProjection reciprocalToRealProjection;
        Backprojection backprojection;
        Sinogram sinogram;
        Refinement refinement;
        Lattice sampleLattice;

        ConsideredPeaksCount consideredPeaksCount;
        AngleResolution angleResolution;
        RefinementType refinementType;
        float maxResolutionForIndexing_1_per_A;
        float finalRefinementTolerance;  //from command line in crystfel
    };
} // namespace pinkIndexer