#ifndef ADAPTIONS_CRYSTFEL_SIMPLE_PROJECTION_H
#define ADAPTIONS_CRYSTFEL_SIMPLE_PROJECTION_H

#include "ExperimentSettings.h"
#include "indexerData.h"
#include "projectionData.h"

#ifdef __cplusplus
namespace pinkIndexer
{
    extern "C" {
#endif

    typedef struct SimpleProjection SimpleProjection;

    SimpleProjection* SimpleProjection_new(ExperimentSettings* experimentSettings);
    void SimpleProjection_delete(SimpleProjection* simpleProjection);

    void project(SimpleProjection* simpleProjection, detectorPeaks_m_t* projectedPeaks_m, const reciprocalPeaks_1_per_A_t* reciprocalPeaks_1_per_A);

#ifdef __cplusplus
    }
}
#endif


#endif
