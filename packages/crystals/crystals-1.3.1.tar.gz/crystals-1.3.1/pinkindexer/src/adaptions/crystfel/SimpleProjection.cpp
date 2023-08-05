#include "adaptions/crystfel/SimpleProjection.h"
#include "SimpleProjection.h"

namespace pinkIndexer
{

    extern "C" SimpleProjection* SimpleProjection_new(ExperimentSettings* experimentSettings)
    {
        return new SimpleProjection(*experimentSettings);
    }

    extern "C" void SimpleProjection_delete(SimpleProjection* simpleProjection)
    {
        delete simpleProjection;
    }

    extern "C" void project(SimpleProjection* simpleProjection, detectorPeaks_m_t* projectedPeaks_m, const reciprocalPeaks_1_per_A_t* reciprocalPeaks_1_per_A)
    {
        Eigen::Matrix3Xf reciprocalPeaks_1_per_A_matrix(3, reciprocalPeaks_1_per_A->peakCount);
        for (int i = 0; i < reciprocalPeaks_1_per_A->peakCount; i++)
        {
            reciprocalPeaks_1_per_A_matrix.col(i) << reciprocalPeaks_1_per_A->coordinates_x[i], reciprocalPeaks_1_per_A->coordinates_y[i],
                reciprocalPeaks_1_per_A->coordinates_z[i];
        }

        Eigen::Matrix2Xf projectedPeaks_m_matrix;
        simpleProjection->project(projectedPeaks_m_matrix, reciprocalPeaks_1_per_A_matrix);

        int peakCount = std::min(MAX_PEAK_COUNT_FOR_PROJECTION, (int)projectedPeaks_m_matrix.cols());
        projectedPeaks_m->peakCount = peakCount;
        for (int i = 0; i < peakCount; i++)
        {
            projectedPeaks_m->coordinates_x[i] = projectedPeaks_m_matrix(0, i);
            projectedPeaks_m->coordinates_y[i] = projectedPeaks_m_matrix(1, i);
        }
    }
} // namespace pinkIndexer