#pragma once

#define EIGEN_DONT_PARALLELIZE

#include "Lattice.h"
#include "ReflectionsInRangeFinder.h"
#include "eigenSTLContainers.h"
#include <Eigen/Dense>
#include <string>
#include <vector>

namespace pinkIndexer
{
    class Sinogram
    {
      public:
        Sinogram(const Lattice& lattice);

        void setSinogramAngleResolution(float angleResolution_deg);

        void computeSinogram(const Eigen::Matrix3Xf& ulsDirections, const Eigen::Matrix2Xf ulsBorderNorms);
        void computeSinogramParallel(const Eigen::Matrix3Xf& ulsDirections, const Eigen::Matrix2Xf ulsBorderNorms, int slaveThreadCount);
        void computeSinogramParallel2(const Eigen::Matrix3Xf& ulsDirections, const Eigen::Matrix2Xf ulsBorderNorms, int slaveThreadCount);

        void getBestRotation(Eigen::AngleAxisf& bestRotation);

        void saveToFile(std::string fileName);

      private:
        void computePartOfSinogramOnePeak(Eigen::Matrix3Xf* candidateReflectionDirections, Eigen::Vector3f* l, int threadCount, int threadNumber);
        void getLocalCenterOfMass(Eigen::Vector3f& centerOfMassSub, const Eigen::Matrix<uint32_t, 3, 1>& centerElementSub);

        ReflectionsInRangeFinder reflectionsInRangeFinder;

        float angleResolution_deg;
        uint32_t sinogramSize_exact, sinogramSize, sinogramCenter;
        float sinogramScale;
        uint32_t anglesCount;
        Eigen::Matrix<uint32_t, 1, 2> strides;
        Eigen::Matrix<uint32_t, 28, 1> dilationOffsets; // actually 27, but padded to be fixed-size-vectorizeable
        Eigen::Array<float, 1, Eigen::Dynamic> sinah, cosah;
        float realToMatrixScaling, realToMatrixOffset;
        Eigen::Matrix<uint8_t, Eigen::Dynamic, 1> sinogram, sinogram_oneMeasuredPeak;

      public:
        EIGEN_MAKE_ALIGNED_OPERATOR_NEW
    };
} // namespace pinkIndexer