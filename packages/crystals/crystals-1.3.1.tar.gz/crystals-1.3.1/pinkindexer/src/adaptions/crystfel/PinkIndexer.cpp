#include "PinkIndexer.h"
#include "adaptions/crystfel/PinkIndexer.h"

namespace pinkIndexer
{
    static float getRefinementDisbalance(Eigen::Array<bool, Eigen::Dynamic, 1>& fittedPeaks, Eigen::Matrix3Xf reciprocalPeaks);
    static float getRefinementDisbalance2(Eigen::Array<bool, Eigen::Dynamic, 1>& fittedPeaks, Eigen::Matrix3Xf reciprocalPeaks);

    extern "C" PinkIndexer* PinkIndexer_new(ExperimentSettings* experimentSettings, consideredPeaksCount_t consideredPeaksCount,
                                            angleResolution_t angleResolution, refinementType_t refinementType, float maxResolutionForIndexing_1_per_A)
    {
        PinkIndexer::ConsideredPeaksCount consideredPeaksCount_enumClass;
        switch (consideredPeaksCount)
        {
            case CONSIDERED_PEAKS_COUNT_veryFew:
                consideredPeaksCount_enumClass = PinkIndexer::ConsideredPeaksCount::veryFew;
                break;
            case CONSIDERED_PEAKS_COUNT_few:
                consideredPeaksCount_enumClass = PinkIndexer::ConsideredPeaksCount::few;
                break;
            case CONSIDERED_PEAKS_COUNT_standard:
                consideredPeaksCount_enumClass = PinkIndexer::ConsideredPeaksCount::standard;
                break;
            case CONSIDERED_PEAKS_COUNT_many:
                consideredPeaksCount_enumClass = PinkIndexer::ConsideredPeaksCount::many;
                break;
            case CONSIDERED_PEAKS_COUNT_manyMany:
                consideredPeaksCount_enumClass = PinkIndexer::ConsideredPeaksCount::manyMany;
                break;

            default:
                consideredPeaksCount_enumClass = PinkIndexer::ConsideredPeaksCount::standard;
                break;
        }

        PinkIndexer::AngleResolution angleResolution_enumClass;
        switch (angleResolution)
        {
            case ANGLE_RESOLUTION_extremelyLoose:
                angleResolution_enumClass = PinkIndexer::AngleResolution::extremelyLoose;
                break;
            case ANGLE_RESOLUTION_loose:
                angleResolution_enumClass = PinkIndexer::AngleResolution::loose;
                break;
            case ANGLE_RESOLUTION_standard:
                angleResolution_enumClass = PinkIndexer::AngleResolution::standard;
                break;
            case ANGLE_RESOLUTION_dense:
                angleResolution_enumClass = PinkIndexer::AngleResolution::dense;
                break;
            case ANGLE_RESOLUTION_extremelyDense:
                angleResolution_enumClass = PinkIndexer::AngleResolution::extremelyDense;
                break;

            default:
                angleResolution_enumClass = PinkIndexer::AngleResolution::standard;
                break;
        }

        PinkIndexer::RefinementType refinementType_enumClass;
        switch (refinementType)
        {
            case REFINEMENT_TYPE_none:
                refinementType_enumClass = PinkIndexer::RefinementType::none;
                break;
            case REFINEMENT_TYPE_fixedLatticeParameters:
                refinementType_enumClass = PinkIndexer::RefinementType::fixedLatticeParameters;
                break;
            case REFINEMENT_TYPE_variableLatticeParameters:
                refinementType_enumClass = PinkIndexer::RefinementType::variableLatticeParameters;
                break;
            case REFINEMENT_TYPE_firstFixedThenVariableLatticeParameters:
                refinementType_enumClass = PinkIndexer::RefinementType::firstFixedThenVariableLatticeParameters;
                break;
            case REFINEMENT_TYPE_firstFixedThenVariableLatticeParametersMultiSeed:
                refinementType_enumClass = PinkIndexer::RefinementType::firstFixedThenVariableLatticeParametersMultiSeed;
                break;
            case REFINEMENT_TYPE_firstFixedThenVariableLatticeParametersCenterAdjustmentMultiSeed:
                refinementType_enumClass = PinkIndexer::RefinementType::firstFixedThenVariableLatticeParametersCenterAdjustmentMultiSeed;
                break;

            default:
                refinementType_enumClass = PinkIndexer::RefinementType::fixedLatticeParameters;
                break;
        }

        return new PinkIndexer(*experimentSettings, consideredPeaksCount_enumClass, angleResolution_enumClass, refinementType_enumClass,
                               maxResolutionForIndexing_1_per_A);
    }

    extern "C" void PinkIndexer_delete(PinkIndexer* pinkIndexer)
    {
        delete pinkIndexer;
    }

    extern "C" int PinkIndexer_indexPattern(PinkIndexer* pinkIndexer, Lattice_t* indexedLattice, float centerShift[2],
                                            reciprocalPeaks_1_per_A_t* meanReciprocalPeaks_1_per_A, const float* intensities, float maxRefinementDisbalance,
                                            int threadCount)
    {
        Eigen::Matrix3Xf meanReciprocalPeaks_1_per_A_matrix(3, meanReciprocalPeaks_1_per_A->peakCount);
        for (int i = 0; i < meanReciprocalPeaks_1_per_A->peakCount; i++)
        {
            meanReciprocalPeaks_1_per_A_matrix.col(i) << meanReciprocalPeaks_1_per_A->coordinates_x[i], meanReciprocalPeaks_1_per_A->coordinates_y[i],
                meanReciprocalPeaks_1_per_A->coordinates_z[i];
        }

        Lattice indexedLattice_class;
        Eigen::Vector2f centerShift_vector;
        Eigen::RowVectorXf intensities_class = Eigen::Map<Eigen::RowVectorXf>((float*)intensities, 1, meanReciprocalPeaks_1_per_A->peakCount);
        Eigen::Array<bool, Eigen::Dynamic, 1> fittedPeaks;
        int matchedPeaksCount = pinkIndexer->indexPattern(indexedLattice_class, centerShift_vector, fittedPeaks, intensities_class,
                                                          meanReciprocalPeaks_1_per_A_matrix, threadCount);

        Eigen::Matrix3f basis = indexedLattice_class.getBasis();
        indexedLattice->ax = basis(0, 0);
        indexedLattice->ay = basis(1, 0);
        indexedLattice->az = basis(2, 0);
        indexedLattice->bx = basis(0, 1);
        indexedLattice->by = basis(1, 1);
        indexedLattice->bz = basis(2, 1);
        indexedLattice->cx = basis(0, 2);
        indexedLattice->cy = basis(1, 2);
        indexedLattice->cz = basis(2, 2);

        centerShift[0] = centerShift_vector.x();
        centerShift[1] = centerShift_vector.y();

        float refinementDisbalance = getRefinementDisbalance(fittedPeaks, meanReciprocalPeaks_1_per_A_matrix);
        float refinementDisbalance2 = getRefinementDisbalance2(fittedPeaks, meanReciprocalPeaks_1_per_A_matrix);
        if (refinementDisbalance > maxRefinementDisbalance || refinementDisbalance2 > maxRefinementDisbalance * 0.5)
        {
            return -1;
        }

        int unfittedPeaksCount = 0;
        for (int i = 0; i < fittedPeaks.size(); i++)
        {
            if (!fittedPeaks[i])
            {
                meanReciprocalPeaks_1_per_A->coordinates_x[unfittedPeaksCount] = meanReciprocalPeaks_1_per_A->coordinates_x[i];
                meanReciprocalPeaks_1_per_A->coordinates_y[unfittedPeaksCount] = meanReciprocalPeaks_1_per_A->coordinates_y[i];
                meanReciprocalPeaks_1_per_A->coordinates_z[unfittedPeaksCount] = meanReciprocalPeaks_1_per_A->coordinates_z[i];

                unfittedPeaksCount++;
            }
        }
        meanReciprocalPeaks_1_per_A->peakCount = unfittedPeaksCount;

        return matchedPeaksCount;
    }

    static float getRefinementDisbalance(Eigen::Array<bool, Eigen::Dynamic, 1>& fittedPeaks, Eigen::Matrix3Xf reciprocalPeaks)
    {
        int fittedCount = fittedPeaks.count();
        int totalCount = fittedPeaks.size();

        if (fittedCount == 0)
        {
            return 2;
        }

        Eigen::Vector2f fittedCenterOfGravity, totalCenterOfGravity;

        totalCenterOfGravity.setZero();
        fittedCenterOfGravity.setZero();
        for (int i = 0; i < totalCount; ++i)
        {
            Eigen::Vector2f normalizedVector = reciprocalPeaks.col(i).head(2).normalized();

            totalCenterOfGravity += normalizedVector;
            if (fittedPeaks[i])
            {
                fittedCenterOfGravity += normalizedVector;
            }
        }

        totalCenterOfGravity /= totalCount;
        fittedCenterOfGravity /= fittedCount;

        float disbalance = (totalCenterOfGravity - fittedCenterOfGravity).norm();
        return disbalance;
    }

    static float getRefinementDisbalance2(Eigen::Array<bool, Eigen::Dynamic, 1>& fittedPeaks, Eigen::Matrix3Xf reciprocalPeaks)
    {
        int fittedCount = fittedPeaks.count();
        int totalCount = fittedPeaks.size();

        if (fittedCount == 0)
        {
            return 2;
        }

        Eigen::Matrix3Xf fittedReciprocalPeaks;
        fittedReciprocalPeaks.resize(3, fittedCount);

        fittedCount = 0;
        for (int i = 0; i < totalCount; ++i)
        {
            if (fittedPeaks[i])
            {
                fittedReciprocalPeaks.col(fittedCount) = reciprocalPeaks.col(i);
                fittedCount++;
            }
        }

        Eigen::Vector3f totalCenterOfGravity = reciprocalPeaks.rowwise().mean();
        float totalMeanDist = (reciprocalPeaks.colwise() - totalCenterOfGravity).cwiseAbs().rowwise().mean().norm();

        Eigen::Vector3f fittedCenterOfGravity = fittedReciprocalPeaks.rowwise().mean();
        float fittedMeanDist = (fittedReciprocalPeaks.colwise() - fittedCenterOfGravity).cwiseAbs().rowwise().mean().norm();

        float disbalance = 1.0f - std::abs(fittedMeanDist / totalMeanDist);
        return disbalance;
    }
} // namespace pinkIndexer