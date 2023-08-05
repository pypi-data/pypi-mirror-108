#pragma once

#include "BadInputException.h"
#include "ExperimentSettings.h"
#include "eigenSTLContainers.h"

namespace pinkIndexer
{
    class ReflectionsInRangeFinder
    {
      public:
        ReflectionsInRangeFinder(const Lattice& lattice);

        void getReflectionsInRanges(EigenSTL::vector_Matrix3Xf& candidateReflectionsDirections, const Eigen::Array2Xf& ranges);

      private:
        Eigen::Matrix3Xf reflectionsDirections_sorted;
        std::vector<float> norms_sorted;
        float maxRadius;
    };
} // namespace pinkIndexer