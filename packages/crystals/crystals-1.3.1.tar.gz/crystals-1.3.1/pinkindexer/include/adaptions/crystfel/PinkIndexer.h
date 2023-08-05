
#ifndef ADAPTIONS_CRYSTFEL_PINK_INDEXER_H
#define ADAPTIONS_CRYSTFEL_PINK_INDEXER_H

#include "ExperimentSettings.h"
#include "indexerData.h"

#ifdef __cplusplus
namespace pinkIndexer
{
    extern "C" {
#endif

    typedef enum
    {
        CONSIDERED_PEAKS_COUNT_veryFew = 0,
        CONSIDERED_PEAKS_COUNT_few = 1,
        CONSIDERED_PEAKS_COUNT_standard = 2,
        CONSIDERED_PEAKS_COUNT_many = 3,
        CONSIDERED_PEAKS_COUNT_manyMany = 4,

        CONSIDERED_PEAKS_COUNT_lastEnum
    } consideredPeaksCount_t;

    typedef enum
    {
        ANGLE_RESOLUTION_extremelyLoose = 0,
        ANGLE_RESOLUTION_loose = 1,
        ANGLE_RESOLUTION_standard = 2,
        ANGLE_RESOLUTION_dense = 3,
        ANGLE_RESOLUTION_extremelyDense = 4,

        ANGLE_RESOLUTION_lastEnum
    } angleResolution_t;

    typedef enum
    {
        REFINEMENT_TYPE_none = 0,
        REFINEMENT_TYPE_fixedLatticeParameters = 1,
        REFINEMENT_TYPE_variableLatticeParameters = 2,
        REFINEMENT_TYPE_firstFixedThenVariableLatticeParameters = 3,
        REFINEMENT_TYPE_firstFixedThenVariableLatticeParametersMultiSeed = 4,
        REFINEMENT_TYPE_firstFixedThenVariableLatticeParametersCenterAdjustmentMultiSeed = 5,
        REFINEMENT_TYPE_lastEnum
    } refinementType_t;

    typedef struct PinkIndexer PinkIndexer;

    PinkIndexer* PinkIndexer_new(ExperimentSettings* experimentSettings, consideredPeaksCount_t consideredPeaksCount, angleResolution_t angleResolution,
                                 refinementType_t refinementType, float maxResolutionForIndexing_1_per_A);
    void PinkIndexer_delete(PinkIndexer* pinkIndexer);

    int PinkIndexer_indexPattern(PinkIndexer* pinkIndexer, Lattice_t* indexedLattice, float centerShift[2],
                                 reciprocalPeaks_1_per_A_t* meanReciprocalPeaks_1_per_A, const float* intensities, float maxRefinementDisbalance,
                                 int threadCount);


#ifdef __cplusplus
    }
}
#endif


#endif