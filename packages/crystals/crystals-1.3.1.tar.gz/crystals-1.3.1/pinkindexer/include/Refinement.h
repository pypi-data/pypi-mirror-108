#pragma once


#include "Backprojection.h"
#include "Lattice.h"
#include "ReciprocalToRealProjection.h"
#include <Eigen/Dense>
#include <vector>

namespace pinkIndexer
{
    class Refinement
    {
      public:
        Refinement(float tolerance);
        Refinement(float tolerance, const Backprojection& backprojection);

        void refineFixedLattice(Lattice& lattice, const Eigen::Matrix3Xf& ulsDirections, const Eigen::Array2Xf& ulsBorderNorms);
        void refineVariableLattice(Lattice& lattice, const Eigen::Matrix3Xf& ulsDirections, const Eigen::Array2Xf& ulsBorderNorms);

        void refineVariableLatticeWithCenter(Lattice& lattice, Eigen::Vector2f& centerShift, const Eigen::Matrix2Xf& detectorPeaks_m);
        void refineCenter(Eigen::Vector2f& centerShift, const Eigen::Matrix3f& basis, const Eigen::Matrix2Xf& detectorPeaks_m, float startStepSize = 20e-6);

        int getFittedPeaksCount(Lattice& lattice, const Eigen::Matrix3Xf& ulsDirections, const Eigen::Array2Xf& ulsBorderNorms);
        int getFittedPeaks(Lattice& lattice, Eigen::Array<bool, Eigen::Dynamic, 1>& fittedPeaks, const Eigen::Matrix3Xf& ulsDirections,
                           const Eigen::Array2Xf& ulsBorderNorms);
        double getMeanDefect(const Eigen::Matrix3f& basis, const Eigen::Matrix3Xf& ulsDirections, const Eigen::Array2Xf& ulsBorderNorms,
                             bool significantChangesToPreviousCall = true);

        void setTolerance(float tolerance)
        {
            this->tolerance = tolerance;
        }
        float getTolerance()
        {
            return tolerance;
        }

      private:
        void getDefects(Eigen::ArrayXf& defects, const Eigen::Matrix3f& basis, const Eigen::Matrix3Xf& ulsDirections, const Eigen::Array2Xf& ulsBorderNorms,
                        bool significantChangesToPreviousCall = true);

        void getCenterShiftedBackprojection(Eigen::Matrix3Xf& ulsDirections, Eigen::Array2Xf& ulsBorderNorms, const Eigen::Matrix2Xf& detectorPeaks_m,
                                            const Eigen::Vector2f& centerShift);

        float tolerance;

        const Backprojection* backprojection;

        // preallocation
        Eigen::ArrayXf defects;
        Eigen::Array2Xf ulsBorderNormsSquared;
        Eigen::Matrix3Xf millerIndices_close;
        Eigen::Matrix3Xf millerIndices_far;
        Eigen::Matrix3Xf candidatePeaks;
        Eigen::RowVectorXf candidatePeaksNormsSquared;
        std::vector<Eigen::Vector3f> millerIndices;
        Eigen::RowVectorXf projectedVectorNorms;
        Eigen::Matrix3Xf defectVectors_absolute;
        Eigen::Matrix3Xf defectVectors_relative;
        Eigen::Array<bool, 1, Eigen::Dynamic> notPredictablePeaks;
        Eigen::ArrayXf meanDefects;
        Eigen::ArrayXf meanDefects_centerAdjustment;
        int validCandidatePeaksCount;
        Eigen::Matrix2Xf detectorPeaks_m_shifted;
        Eigen::Matrix3Xf ulsDirections;
        Eigen::Array2Xf ulsBorderNorms;
    };
} // namespace pinkIndexer